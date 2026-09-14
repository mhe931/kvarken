"""Bounded asynchronous STAC transformation and persistence orchestration."""

import asyncio
from collections.abc import Iterable
from dataclasses import dataclass

from .models import EOScene
from .provenance import FileProvenanceSink, ProvenanceRecord
from .stac import STACClient, STACItem
from .transform import transform_stac_to_scene


@dataclass(frozen=True, slots=True)
class ConcurrentIngestionResult:
    scene: EOScene
    provenance: ProvenanceRecord


class ConcurrentEOIngestor:
    """Transform and persist items with an explicit concurrency ceiling."""

    def __init__(
        self,
        adapter: STACClient,
        sink: FileProvenanceSink,
        *,
        max_workers: int = 4,
    ) -> None:
        if max_workers < 1:
            raise ValueError("max_workers must be at least one")
        self._adapter = adapter
        self._sink = sink
        self._semaphore = asyncio.Semaphore(max_workers)

    async def ingest(self, items: Iterable[STACItem]) -> list[ConcurrentIngestionResult]:
        async def worker(item: STACItem) -> ConcurrentIngestionResult:
            async with self._semaphore:
                scene = transform_stac_to_scene(item.raw_payload)
                provenance = await self._sink.store_async(
                    source_id=item.item_id,
                    collection=item.collection,
                    source_uri=item.source_uri,
                    payload=item.raw_payload,
                )
                return ConcurrentIngestionResult(scene, provenance)

        return list(await asyncio.gather(*(worker(item) for item in items)))

    async def search_and_ingest(self, **search_kwargs: object) -> list[ConcurrentIngestionResult]:
        items = await self._adapter.search(**search_kwargs)
        return await self.ingest(items)
