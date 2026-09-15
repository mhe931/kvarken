import pytest

from kvarken_eo.cdse import CDSEClient, CDSETokenProvider


class TokenTransport:
    def __init__(self):
        self.calls = 0

    async def request(self, url, client_id, client_secret, request_timeout):
        self.calls += 1
        return {"access_token": f"token-{self.calls}", "expires_in": 100}


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
async def test_cdse_client_uses_offline_transport_and_stac_validation():
    provider = CDSETokenProvider(
        "https://identity.invalid/token", "client", "secret", transport=TokenTransport()
    )
    client = CDSEClient("https://cdse.invalid", provider, transport=STACTransport())

    items = await client.search(collections=("sentinel-2-l2a",))

    assert [item.item_id for item in items] == ["cdse-1"]
