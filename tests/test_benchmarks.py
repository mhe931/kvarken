import asyncio
import json
from pathlib import Path

import pytest

from kvarken_eo.concurrent import ConcurrentEOIngestor
from kvarken_eo.ingestion import RateLimitExceeded, RetryPolicy
from kvarken_eo.provenance import FileProvenanceSink
from kvarken_eo.stac import STACClient

FIXTURE = Path(__file__).parent / "fixtures" / "stac_search_page_1.json"


class BurstRateLimitedTransport:
    def __init__(self, page, failures, latency):
        self.page = page
        self.failures = failures
        self.latency = latency
        self.calls = 0

    async def request(self, method, url, payload, request_timeout):
        self.calls += 1
        await asyncio.sleep(self.latency)
        if self.failures:
            self.failures -= 1
            raise RateLimitExceeded(retry_after=0)
        return self.page


@pytest.mark.asyncio
async def test_rate_limit_burst_recovers_without_dropped_records(tmp_path):
    template = json.loads(FIXTURE.read_text(encoding="utf-8"))["features"][0]
    page = {"type": "FeatureCollection", "features": [], "links": []}
    for index in range(12):
        item = json.loads(json.dumps(template))
        item["id"] = f"burst-{index}"
        page["features"].append(item)
    transport = BurstRateLimitedTransport(page, failures=2, latency=0.001)
    adapter = STACClient(
        "https://stac.example.invalid",
        transport,
        retry_policy=RetryPolicy(
            max_attempts=4,
            base_delay=0.001,
            max_delay=0.002,
            jitter_ratio=0.5,
        ),
    )
    sink = FileProvenanceSink(tmp_path)

    results = await ConcurrentEOIngestor(adapter, sink, max_workers=4).search_and_ingest()

    records = (tmp_path / "manifest.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(results) == len(page["features"]) == 12
    assert len(records) == 12
    assert transport.calls == 3
    assert len({json.loads(record)["source_id"] for record in records}) == 12
