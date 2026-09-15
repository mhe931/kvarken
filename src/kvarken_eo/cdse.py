"""Dependency-free CDSE OAuth2 authentication and STAC adapter."""

import asyncio
import base64
import json
import time
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .ingestion import FetchTimeout, RateLimitExceeded, RetryPolicy
from .stac import STACClient, STACTransport


@dataclass(frozen=True, slots=True)
class OAuthToken:
    access_token: str
    expires_at: float

    @classmethod
    def from_response(cls, response: Mapping[str, object], now: float) -> "OAuthToken":
        token = response.get("access_token")
        expires_in = response.get("expires_in", 3600)
        if not isinstance(token, str) or not token:
            raise ValueError("OAuth response has no access_token")
        try:
            lifetime = float(expires_in)
        except (TypeError, ValueError) as error:
            raise ValueError("OAuth response has invalid expires_in") from error
        if lifetime <= 0:
            raise ValueError("OAuth token lifetime must be positive")
        return cls(token, now + lifetime)


class OAuthTransport(Protocol):
    async def request(
        self, url: str, client_id: str, client_secret: str, request_timeout: float
    ) -> Mapping[str, object]:
        """Exchange client credentials for a token."""


class UrllibOAuthTransport:
    async def request(
        self, url: str, client_id: str, client_secret: str, request_timeout: float
    ) -> Mapping[str, object]:
        return await asyncio.to_thread(
            self._request, url, client_id, client_secret, request_timeout
        )

    @staticmethod
    def _request(
        url: str, client_id: str, client_secret: str, request_timeout: float
    ) -> Mapping[str, object]:
        credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        request = Request(
            url,
            data=urlencode({"grant_type": "client_credentials"}).encode(),
            headers={
                "Accept": "application/json",
                "Authorization": f"Basic {credentials}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            method="POST",
        )
        try:
            with urlopen(request, timeout=request_timeout) as response:
                decoded = json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            if error.code == 429:
                raise RateLimitExceeded() from error
            raise FetchTimeout(f"OAuth endpoint returned HTTP {error.code}") from error
        except (TimeoutError, URLError) as error:
            raise FetchTimeout("OAuth request failed") from error
        if not isinstance(decoded, Mapping):
            raise ValueError("OAuth response must be a JSON object")
        return decoded


class CDSETokenProvider:
    def __init__(
        self,
        token_url: str,
        client_id: str,
        client_secret: str,
        *,
        transport: OAuthTransport | None = None,
        timeout: float = 20.0,
        clock: callable = time.time,
        refresh_skew: float = 30.0,
        retry_policy: RetryPolicy | None = None,
    ) -> None:
        if not token_url.strip() or not client_id or not client_secret:
            raise ValueError("token URL and client credentials are required")
        if timeout <= 0 or refresh_skew < 0:
            raise ValueError("timeout must be positive and refresh_skew non-negative")
        self._url = token_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._transport = transport or UrllibOAuthTransport()
        self._timeout = timeout
        self._clock = clock
        self._refresh_skew = refresh_skew
        self._retry_policy = retry_policy or RetryPolicy()
        self._token: OAuthToken | None = None
        self._lock = asyncio.Lock()

    async def get_token(self) -> str:
        async with self._lock:
            now = self._clock()
            if self._token is None or self._token.expires_at - self._refresh_skew <= now:
                response = await self._request_token()
                self._token = OAuthToken.from_response(response, now)
            return self._token.access_token

    async def _request_token(self) -> Mapping[str, object]:
        for attempt in range(1, self._retry_policy.max_attempts + 1):
            try:
                return await self._transport.request(
                    self._url, self._client_id, self._client_secret, self._timeout
                )
            except (FetchTimeout, RateLimitExceeded) as error:
                if attempt == self._retry_policy.max_attempts:
                    raise
                delay = error.retry_after if isinstance(error, RateLimitExceeded) else None
                await asyncio.sleep(
                    min(self._retry_policy.max_delay, delay)
                    if delay is not None
                    else self._retry_policy.delay_for(attempt)
                )
        raise AssertionError("token retry loop must return or raise")


class AuthenticatedSTACTransport:
    def __init__(self, inner: STACTransport, token_provider: CDSETokenProvider) -> None:
        self._inner = inner
        self._token_provider = token_provider

    async def request(self, method, url, payload, request_timeout):
        token = await self._token_provider.get_token()
        authenticated_url = url
        if hasattr(self._inner, "set_authorization"):
            self._inner.set_authorization(token)
        return await self._inner.request(method, authenticated_url, payload, request_timeout)


class CDSEClient(STACClient):
    """STAC client configured for CDSE OAuth2 client credentials."""

    def __init__(
        self,
        api_url: str,
        token_provider: CDSETokenProvider,
        transport: STACTransport | None = None,
        **kwargs: object,
    ) -> None:
        super().__init__(
            api_url,
            AuthenticatedSTACTransport(transport or BearerSTACTransport(), token_provider),
            **kwargs,
        )


class BearerSTACTransport:
    """HTTP transport used by CDSE, with the current bearer token."""

    def __init__(self) -> None:
        self._authorization = ""

    def set_authorization(self, token: str) -> None:
        self._authorization = f"Bearer {token}"

    async def request(self, method, url, payload, request_timeout):
        return await asyncio.to_thread(self._request, method, url, payload, request_timeout)

    def _request(self, method, url, payload, request_timeout):
        body = json.dumps(payload).encode() if payload is not None else None
        request = Request(
            url,
            data=body,
            headers={
                "Accept": "application/geo+json, application/json",
                "Content-Type": "application/json",
                "Authorization": self._authorization,
            },
            method=method,
        )
        try:
            with urlopen(request, timeout=request_timeout) as response:
                decoded = json.loads(response.read().decode())
        except (TimeoutError, URLError) as error:
            raise FetchTimeout("CDSE request failed") from error
        if not isinstance(decoded, Mapping):
            raise ValueError("CDSE response must be a JSON object")
        return decoded
