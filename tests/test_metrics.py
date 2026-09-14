import json
from pathlib import Path

import pytest

from kvarken_eo import ConcurrentEOIngestor, FileProvenanceSink, IngestionMetrics
from kvarken_eo.stac import STACItem

FIXTURE = Path(__file__).parent / "fixtures" / "stac_search_page_1.json"


def make_item(index: int, attempts: int = 1) -> STACItem:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))["features"][0]
    payload["id"] = f"metrics-{index}"
    return STACItem(
        payload["id"],
        payload["collection"],
        "fixture://metrics",
        payload["properties"],
        payload,
        attempts,
    )


class UnusedAdapter:
    async def search(self, **kwargs):
        return []


@pytest.mark.asyncio
async def test_ingestion_metrics_report_counts_bytes_retries_and_rate(tmp_path):
    ingestor = ConcurrentEOIngestor(
        UnusedAdapter(),
        FileProvenanceSink(tmp_path),
        max_workers=2,
    )

    results, metrics = await ingestor.ingest_with_metrics([make_item(1), make_item(2, attempts=3)])

    expected_bytes = sum(
        len(
            json.dumps(
                item.raw_payload,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=True,
            ).encode("utf-8")
        )
        for item in [make_item(1), make_item(2, attempts=3)]
    )
    assert len(results) == 2
    assert isinstance(metrics, IngestionMetrics)
    assert metrics.scenes_ingested == 2
    assert metrics.retry_count == 2
    assert metrics.failure_count == 0
    assert metrics.payload_bytes == expected_bytes
    assert metrics.elapsed_seconds >= 0
    assert metrics.throughput_items_per_second >= 0
    assert ingestor.last_metrics == metrics


@pytest.mark.asyncio
async def test_search_and_ingest_exposes_metrics_on_legacy_result_api(tmp_path):
    class Adapter:
        async def search(self, **kwargs):
            return [make_item(1)]

    ingestor = ConcurrentEOIngestor(Adapter(), FileProvenanceSink(tmp_path))

    results = await ingestor.search_and_ingest(collections=("sentinel-2-l2a",))

    assert len(results) == 1
    assert ingestor.last_metrics.scenes_ingested == 1
    assert ingestor.last_metrics.payload_bytes > 0
