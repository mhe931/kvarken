import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from kvarken_eo.ingestion import FetchTimeout, RateLimitExceeded, RetryPolicy
from kvarken_eo.models import PayloadValidationError
from kvarken_eo.provenance import FileProvenanceSink
from kvarken_eo.stac import STACClient

FIXTURES = Path(__file__).parent / "fixtures"


class FakeTransport:
    def __init__(self, responses):
        self.responses = list(responses)
        self.requests = []

    async def request(self, method, url, payload, request_timeout):
        self.requests.append((method, url, payload, request_timeout))
        response = self.responses.pop(0)
        if isinstance(response, BaseException):
            raise response
        return response


def fixture(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


@pytest.mark.asyncio
async def test_search_fetches_pages_and_preserves_query():
    transport = FakeTransport(
        [fixture("stac_search_page_1.json"), fixture("stac_search_page_2.json")]
    )
    client = STACClient(
        "https://stac.example.invalid",
        transport,
        retry_policy=RetryPolicy(base_delay=0, max_delay=0),
    )

    items = await client.search(collections=("sentinel-2-l2a",), bbox=(21, 63, 21.1, 63.1), limit=1)

    assert [item.item_id for item in items] == [
        "S2A_MSIL2A_20260914T100031_N0511_R122_T34WDL_20260914T123456",
        "S2B_MSIL2A_20260915T100029_N0511_R122_T34WDL_20260915T123456",
    ]
    assert transport.requests[0][0] == "POST"
    assert transport.requests[0][2]["collections"] == ["sentinel-2-l2a"]
    assert transport.requests[1][0] == "GET"


@pytest.mark.asyncio
async def test_search_retries_timeout_and_rate_limit():
    page = fixture("stac_search_page_1.json")
    page["links"] = []
    transport = FakeTransport([FetchTimeout(), RateLimitExceeded(retry_after=0), page])
    client = STACClient(
        "https://stac.example.invalid",
        transport,
        retry_policy=RetryPolicy(base_delay=0, max_delay=0),
    )

    items = await client.search()

    assert len(items) == 1
    assert len(transport.requests) == 3


@pytest.mark.asyncio
async def test_search_rejects_invalid_stac_schema():
    transport = FakeTransport(
        [{"type": "FeatureCollection", "features": [{"type": "Feature", "id": "broken"}]}]
    )

    with pytest.raises(PayloadValidationError):
        await STACClient("https://stac.example.invalid", transport).search()


def test_provenance_sink_writes_hash_and_audit_record(tmp_path):
    payload = fixture("stac_search_page_1.json")["features"][0]
    sink = FileProvenanceSink(tmp_path)
    timestamp = datetime(2026, 9, 14, 12, tzinfo=UTC)

    record = sink.store(
        source_id=payload["id"],
        collection=payload["collection"],
        source_uri="https://stac.example.invalid/search",
        payload=payload,
        attempts=2,
        ingested_at=timestamp,
    )

    assert record.payload_sha256 in record.raw_payload_path
    assert (tmp_path / record.raw_payload_path).exists()
    audit = json.loads((tmp_path / "manifest.jsonl").read_text(encoding="utf-8"))
    assert audit["source_id"] == payload["id"]
    assert audit["attempts"] == 2
    assert audit["ingested_at"] == "2026-09-14T12:00:00+00:00"
