import pytest

from kvarken_eo.cdse import CDSEClient, CDSETokenProvider
from kvarken_eo.ingestion import FetchTimeout, RateLimitExceeded, RetryPolicy


class TokenTransport:
    def __init__(self):
        self.calls = 0

    async def request(self, url, client_id, client_secret, request_timeout):
        self.calls += 1
        return {"access_token": f"token-{self.calls}", "expires_in": 100}


class FailureTransport:
    def __init__(self, failures):
        self.responses = list(failures)

    async def request(self, url, client_id, client_secret, request_timeout):
        response = self.responses.pop(0)
        if isinstance(response, BaseException):
            raise response
        return response


class STACTransport:
    async def request(self, method, url, payload, request_timeout):
        return {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "id": "cdse-1",
                    "collection": "sentinel-2-l2a",
                    "properties": {"datetime": "2026-09-14T12:00:00Z"},
                }
            ],
            "links": [],
        }


@pytest.mark.asyncio
async def test_token_provider_caches_and_refreshes_tokens():
    clock = [100.0]
    transport = TokenTransport()
    provider = CDSETokenProvider(
        "https://identity.invalid/token",
        "client",
        "secret",
        transport=transport,
        clock=lambda: clock[0],
        refresh_skew=10,
    )

    assert await provider.get_token() == "token-1"
    assert await provider.get_token() == "token-1"
    clock[0] = 191
    assert await provider.get_token() == "token-2"
    assert transport.calls == 2


@pytest.mark.asyncio
async def test_token_provider_retries_rate_limit_then_caches_token():
    provider = CDSETokenProvider(
        "https://identity.invalid/token",
        "client",
        "secret",
        transport=FailureTransport(
            [RateLimitExceeded(retry_after=0), {"access_token": "recovered", "expires_in": 100}]
        ),
        retry_policy=RetryPolicy(max_attempts=2, base_delay=0, max_delay=0),
    )

    assert await provider.get_token() == "recovered"


@pytest.mark.asyncio
async def test_token_provider_retries_timeout_and_rejects_invalid_response():
    provider = CDSETokenProvider(
        "https://identity.invalid/token",
        "client",
        "secret",
        transport=FailureTransport([FetchTimeout(), {"access_token": "", "expires_in": 100}]),
        retry_policy=RetryPolicy(max_attempts=2, base_delay=0, max_delay=0),
    )

    with pytest.raises(ValueError, match="access_token"):
        await provider.get_token()


@pytest.mark.asyncio
async def test_token_provider_propagates_exhausted_network_timeout():
    provider = CDSETokenProvider(
        "https://identity.invalid/token",
        "client",
        "secret",
        transport=FailureTransport([FetchTimeout(), FetchTimeout()]),
        retry_policy=RetryPolicy(max_attempts=2, base_delay=0, max_delay=0),
    )

    with pytest.raises(FetchTimeout):
        await provider.get_token()


@pytest.mark.asyncio
async def test_cdse_client_uses_offline_transport_and_stac_validation():
    provider = CDSETokenProvider(
        "https://identity.invalid/token", "client", "secret", transport=TokenTransport()
    )
    client = CDSEClient("https://cdse.invalid", provider, transport=STACTransport())

    items = await client.search(collections=("sentinel-2-l2a",))

    assert [item.item_id for item in items] == ["cdse-1"]
