"""Async STAC search adapter with bounded transient-failure handling."""

import asyncio
import json
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .ingestion import FetchTimeout, RateLimitExceeded, RetryPolicy
from .models import PayloadValidationError


class STACTransport(Protocol):
    async def request(
        self,
        method: str,
        url: str,
        payload: Mapping[str, object] | None,
        request_timeout: float,
    ) -> Mapping[str, object]:
        """Perform one STAC request and return decoded JSON."""


class UrllibSTACTransport:
    """Small dependency-free transport for public STAC APIs."""

    async def request(
        self,
        method: str,
        url: str,
        payload: Mapping[str, object] | None,
        request_timeout: float,
    ) -> Mapping[str, object]:
        return await asyncio.to_thread(self._request, method, url, payload, request_timeout)

    @staticmethod
    def _request(
        method: str,
        url: str,
        payload: Mapping[str, object] | None,
        request_timeout: float,
    ) -> Mapping[str, object]:
        body = json.dumps(payload).encode("utf-8") if payload is not None else None
        request = Request(
            url,
            data=body,
            headers={
                "Accept": "application/geo+json, application/json",
                "Content-Type": "application/json",
            },
            method=method,
        )
        try:
            with urlopen(request, timeout=request_timeout) as response:
                decoded = json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            if error.code == 429:
                retry_after = error.headers.get("Retry-After")
                raise RateLimitExceeded(float(retry_after) if retry_after else None) from error
            raise URLError(f"STAC endpoint returned HTTP {error.code}") from error
        except TimeoutError as error:
            raise FetchTimeout("STAC request timed out") from error
        except URLError as error:
            raise FetchTimeout("STAC request failed") from error
        if not isinstance(decoded, Mapping):
            raise PayloadValidationError("STAC response must be a JSON object")
        return decoded


@dataclass(frozen=True, slots=True)
class STACItem:
    item_id: str
    collection: str
    source_uri: str
    properties: Mapping[str, object]
    raw_payload: Mapping[str, object]


class STACClient:
    def __init__(
        self,
        api_url: str,
        transport: STACTransport | None = None,
        *,
        timeout: float = 20.0,
        retry_policy: RetryPolicy | None = None,
    ) -> None:
        if not api_url.strip():
            raise ValueError("api_url must be non-empty")
        if timeout <= 0:
            raise ValueError("timeout must be positive")
        self._search_url = api_url.rstrip("/") + "/search"
        self._transport = transport or UrllibSTACTransport()
        self._timeout = timeout
        self._retry_policy = retry_policy or RetryPolicy()

    async def search(
        self,
        *,
        collections: tuple[str, ...] = (),
        bbox: tuple[float, float, float, float] | None = None,
        datetime_range: str | None = None,
        limit: int = 100,
    ) -> list[STACItem]:
        if limit < 1:
            raise ValueError("limit must be positive")
        query: dict[str, object] = {"limit": limit}
        if collections:
            query["collections"] = list(collections)
        if bbox is not None:
            if len(bbox) != 4:
                raise ValueError("bbox must contain four coordinates")
            query["bbox"] = list(bbox)
        if datetime_range is not None:
            query["datetime"] = datetime_range

        items: list[STACItem] = []
        url = self._search_url
        payload: Mapping[str, object] | None = query
        method = "POST"
        while url:
            response = await self._request_with_retry(method, url, payload)
            items.extend(self._parse_items(response, url))
            next_link = self._next_link(response)
            url = next_link
            payload = None
            method = "GET"
        return items

    async def _request_with_retry(
        self, method: str, url: str, payload: Mapping[str, object] | None
    ) -> Mapping[str, object]:
        for attempt in range(1, self._retry_policy.max_attempts + 1):
            try:
                return await self._transport.request(method, url, payload, self._timeout)
            except (FetchTimeout, RateLimitExceeded) as error:
                if attempt == self._retry_policy.max_attempts:
                    raise
                delay = error.retry_after if isinstance(error, RateLimitExceeded) else None
                await asyncio.sleep(
                    min(self._retry_policy.max_delay, delay)
                    if delay is not None
                    else self._retry_policy.delay_for(attempt)
                )
        raise AssertionError("retry loop must return or raise")

    @staticmethod
    def _parse_items(response: Mapping[str, object], source_uri: str) -> list[STACItem]:
        if response.get("type") != "FeatureCollection":
            raise PayloadValidationError("STAC response must be a FeatureCollection")
        raw_items = response.get("features")
        if not isinstance(raw_items, list):
            raise PayloadValidationError("STAC response features must be a list")
        parsed: list[STACItem] = []
        for raw_item in raw_items:
            if not isinstance(raw_item, Mapping) or raw_item.get("type") != "Feature":
                raise PayloadValidationError("STAC feature must be a GeoJSON Feature")
            item_id = raw_item.get("id")
            collection = raw_item.get("collection")
            properties = raw_item.get("properties")
            if (
                not isinstance(item_id, str)
                or not item_id
                or not isinstance(collection, str)
                or not collection
                or not isinstance(properties, Mapping)
            ):
                raise PayloadValidationError("STAC feature has invalid identity or properties")
            parsed.append(STACItem(item_id, collection, source_uri, properties, raw_item))
        return parsed

    @staticmethod
    def _next_link(response: Mapping[str, object]) -> str | None:
        links = response.get("links", [])
        if not isinstance(links, list):
            raise PayloadValidationError("STAC response links must be a list")
        for link in links:
            if isinstance(link, Mapping) and link.get("rel") == "next":
                href = link.get("href")
                if not isinstance(href, str) or not href:
                    raise PayloadValidationError("STAC next link must have a valid href")
                return href
        return None
