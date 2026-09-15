import asyncio
import json
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta
from pathlib import Path
from time import perf_counter

import pytest

from kvarken_eo import EOScene, SpatialCatalog
from kvarken_eo.concurrent import ConcurrentEOIngestor
from kvarken_eo.provenance import FileProvenanceSink
from kvarken_eo.stac import STACItem


def _scene(index: int) -> EOScene:
    x = 21.0 + (index % 8) * 0.01
    y = 63.0 + (index % 8) * 0.01
    return EOScene(
        f"thread-scene-{index}",
        "sentinel-2",
        datetime(2026, 1, 1, tzinfo=UTC) + timedelta(minutes=index),
        float(index % 25),
        ((x, y), (x + 0.01, y), (x + 0.01, y + 0.01), (x, y)),
        (x, y, x + 0.01, y + 0.01),
        assets={"thumbnail": f"fixture://{index}.jpg"},
    )


def test_catalog_serializes_multithreaded_upserts_and_queries(tmp_path: Path):
    path = tmp_path / "threaded.sqlite"
    scenes = [_scene(index) for index in range(120)]
    with SpatialCatalog(path) as catalog:

        def index_batch(batch: list[EOScene]) -> None:
            for scene in batch:
                catalog.index_scene(scene)

        batches = [scenes[offset : offset + 15] for offset in range(0, len(scenes), 15)]
        with ThreadPoolExecutor(max_workers=8) as executor:
            list(executor.map(index_batch, batches))

        def query_batch(_: int) -> int:
            return len(catalog.query_scenes(max_cloud_cover=20))

        with ThreadPoolExecutor(max_workers=8) as executor:
            counts = list(executor.map(query_batch, range(32)))

        assert len(catalog.scene_ids()) == len(scenes)
        assert counts == [len([scene for scene in scenes if scene.cloud_cover <= 20])] * 32


def test_wal_mixed_read_write_throughput_and_durability(tmp_path: Path):
    path = tmp_path / "wal-contention.sqlite"
    initial = [_scene(index) for index in range(40)]
    with SpatialCatalog(path) as catalog:
        catalog.index_scenes(initial)

    errors: list[BaseException] = []
    read_latencies: list[float] = []

    def writer() -> int:
        try:
            with SpatialCatalog(path) as catalog:
                for index in range(40, 100):
                    catalog.index_scene(_scene(index))
            return 60
        except BaseException as error:
            errors.append(error)
            return 0

    def reader(_: int) -> int:
        try:
            with SpatialCatalog(path) as catalog:
                started = perf_counter()
                count = 0
                for _ in range(12):
                    count = len(catalog.query_scenes(max_cloud_cover=20))
                read_latencies.append((perf_counter() - started) * 1000)
                return count
        except BaseException as error:
            errors.append(error)
            return 0

    started = perf_counter()
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(reader, index) for index in range(4)]
        futures.append(executor.submit(writer))
        results = [future.result() for future in futures]
    elapsed = perf_counter() - started

    assert not errors
    initial_query_count = len([scene for scene in initial if scene.cloud_cover <= 20])
    final_query_count = len([_scene(index) for index in range(100) if index % 25 <= 20])
    assert all(initial_query_count <= count <= final_query_count for count in results[:4])
    assert results[4] == 60
    assert read_latencies
    assert elapsed < 5.0
    with SpatialCatalog(path) as catalog:
        assert len(catalog.scene_ids()) == 100
    with sqlite3.connect(path) as connection:
        assert connection.execute("PRAGMA journal_mode").fetchone()[0].lower() == "wal"


@pytest.mark.asyncio
async def test_ingestor_stress_never_exceeds_worker_limit(tmp_path: Path):
    first = {
        "type": "Feature",
        "id": "stress-template",
        "collection": "sentinel-2-l2a",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[21.0, 63.0], [21.1, 63.0], [21.1, 63.1], [21.0, 63.0]]],
        },
        "bbox": [21.0, 63.0, 21.1, 63.1],
        "properties": {
            "datetime": "2026-09-14T10:00:31Z",
            "eo:cloud_cover": 4.2,
            "platform": "sentinel-2a",
        },
        "assets": {"thumbnail": {"href": "fixture://thumbnail.jpg"}},
    }
    items = []
    for index in range(48):
        item = json.loads(json.dumps(first))
        item["id"] = f"stress-{index}"
        items.append(
            STACItem(
                item["id"],
                item["collection"],
                "fixture://stress",
                item["properties"],
                item,
            )
        )

    class TrackedSink(FileProvenanceSink):
        def __init__(self, root: Path) -> None:
            super().__init__(root)
            self.active = 0
            self.maximum = 0

        async def store_async(self, **kwargs: object):
            self.active += 1
            self.maximum = max(self.maximum, self.active)
            await asyncio.sleep(0)
            try:
                return await super().store_async(**kwargs)
            finally:
                self.active -= 1

    sink = TrackedSink(tmp_path / "provenance")
    ingestor = ConcurrentEOIngestor(adapter=object(), sink=sink, max_workers=3)

    results, metrics = await ingestor.ingest_with_metrics(items)

    assert len(results) == 48
    assert metrics.scenes_ingested == 48
    assert sink.maximum <= 3
