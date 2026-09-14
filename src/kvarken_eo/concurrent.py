"""Bounded asynchronous STAC transformation and persistence orchestration."""

import asyncio
import json
import time
from collections.abc import Iterable
from dataclasses import dataclass

from .catalog import SpatialCatalog
from .models import EOScene
from .provenance import FileProvenanceSink, ProvenanceRecord
from .stac import STACClient, STACItem
from .transform import transform_stac_to_scene


@dataclass(frozen=True, slots=True)
class ConcurrentIngestionResult:
    scene: EOScene
    provenance: ProvenanceRecord


@dataclass(frozen=True, slots=True)
class IngestionMetrics:
    """Structured summary for one batch ingestion run."""

    scenes_ingested: int
    elapsed_seconds: float
    throughput_items_per_second: float
    failure_count: int
    retry_count: int
    payload_bytes: int


class ConcurrentEOIngestor:
    """Transform and persist items with an explicit concurrency ceiling."""

    def __init__(
        self,
        adapter: STACClient,
        sink: FileProvenanceSink,
        *,
        max_workers: int = 4,
        catalog: SpatialCatalog | None = None,
    ) -> None:
        if max_workers < 1:
            raise ValueError("max_workers must be at least one")
        self._adapter = adapter
        self._sink = sink
        self._semaphore = asyncio.Semaphore(max_workers)
        self._catalog = catalog
        self._last_metrics = IngestionMetrics(0, 0.0, 0.0, 0, 0, 0)

    async def ingest(self, items: Iterable[STACItem]) -> list[ConcurrentIngestionResult]:
        results, _ = await self.ingest_with_metrics(items)
        return results

    @property
    def last_metrics(self) -> IngestionMetrics:
        return self._last_metrics

    async def ingest_with_metrics(
        self, items: Iterable[STACItem]
    ) -> tuple[list[ConcurrentIngestionResult], IngestionMetrics]:
        started = time.perf_counter()
        failures = 0
        retries = 0
        payload_bytes = 0

        async def worker(item: STACItem) -> ConcurrentIngestionResult:
            nonlocal failures, retries, payload_bytes
            async with self._semaphore:
                try:
                    scene = transform_stac_to_scene(item.raw_payload)
                    provenance = await self._sink.store_async(
                        source_id=item.item_id,
                        collection=item.collection,
                        source_uri=item.source_uri,
                        payload=item.raw_payload,
                    )
                    if self._catalog is not None:
                        await asyncio.to_thread(self._catalog.index_scene, scene)
                    retries += max(0, item.attempts - 1)
                    payload_bytes += len(
                        json.dumps(
                            item.raw_payload,
                            sort_keys=True,
                            separators=(",", ":"),
                            ensure_ascii=True,
                        ).encode("utf-8")
                    )
                    return ConcurrentIngestionResult(scene, provenance)
                except Exception:
                    failures += 1
                    raise

        results = list(await asyncio.gather(*(worker(item) for item in items)))
        elapsed = time.perf_counter() - started
        metrics = IngestionMetrics(
            scenes_ingested=len(results),
            elapsed_seconds=elapsed,
            throughput_items_per_second=len(results) / elapsed if elapsed else 0.0,
            failure_count=failures,
            retry_count=retries,
            payload_bytes=payload_bytes,
        )
        self._last_metrics = metrics
        return results, metrics

    async def search_and_ingest(self, **search_kwargs: object) -> list[ConcurrentIngestionResult]:
        items = await self._adapter.search(**search_kwargs)
        return await self.ingest(items)
