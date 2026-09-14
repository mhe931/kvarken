import asyncio
import json
from pathlib import Path

import pytest

from kvarken_eo.concurrent import ConcurrentEOIngestor
from kvarken_eo.ingestion import RetryPolicy
from kvarken_eo.provenance import FileProvenanceSink
from kvarken_eo.stac import STACClient
from kvarken_eo.transform import transform_stac_to_scene

FIXTURES = Path(__file__).parent / "fixtures"


def item_fixture():
    return json.loads((FIXTURES / "stac_search_page_1.json").read_text(encoding="utf-8"))[
        "features"
    ][0]


class SinglePageTransport:
    def __init__(self, page):
        self.page = page

    async def request(self, method, url, payload, request_timeout):
        return self.page


def test_transform_stac_item_normalizes_spatial_and_optional_fields():
    item = item_fixture()

    scene = transform_stac_to_scene(item)

    assert scene.scene_id == item["id"]
    assert scene.platform == "sentinel-2a"
    assert scene.epsg == 4326
    assert scene.bbox == (21.0, 63.0, 21.1, 63.1)
    assert scene.assets["thumbnail"].endswith(".jpg")
    assert scene.footprint[0] == (21.0, 63.0)


def test_transform_defaults_missing_cloud_cover_and_uses_bbox():
    item = item_fixture()
    item["properties"].pop("eo:cloud_cover")
    item["geometry"] = None

    scene = transform_stac_to_scene(item)

    assert scene.cloud_cover == 0
    assert len(scene.footprint) == 4


@pytest.mark.asyncio
async def test_concurrent_ingestor_writes_every_item_without_corrupting_manifest(tmp_path):
    first = item_fixture()
    second = json.loads(json.dumps(first))
    second["id"] = "second-scene"
    second["properties"]["datetime"] = "2026-09-15T10:00:31Z"
    page = {"type": "FeatureCollection", "features": [first, second], "links": []}
    adapter = STACClient(
        "https://stac.example.invalid",
        SinglePageTransport(page),
        retry_policy=RetryPolicy(base_delay=0, max_delay=0),
    )
    sink = FileProvenanceSink(tmp_path)
    ingestor = ConcurrentEOIngestor(adapter, sink, max_workers=2)

    results = await ingestor.search_and_ingest()

    assert {result.scene.scene_id for result in results} == {"second-scene", first["id"]}
    records = [
        json.loads(line)
        for line in (tmp_path / "manifest.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert {record["source_id"] for record in records} == {"second-scene", first["id"]}
    assert len(records) == 2
    assert all((tmp_path / record["raw_payload_path"]).exists() for record in records)


@pytest.mark.asyncio
async def test_concurrent_ingestor_respects_worker_bound(tmp_path):
    class SlowSink(FileProvenanceSink):
        def __init__(self, root):
            super().__init__(root)
            self.active = 0
            self.maximum = 0

        async def store_async(self, **kwargs):
            self.active += 1
            self.maximum = max(self.maximum, self.active)
            await asyncio.sleep(0)
            result = await super().store_async(**kwargs)
            self.active -= 1
            return result

    first = item_fixture()
    items = []
    for index in range(4):
        item = json.loads(json.dumps(first))
        item["id"] = f"scene-{index}"
        items.append(item)
    from kvarken_eo.stac import STACItem

    sink = SlowSink(tmp_path)
    ingestor = ConcurrentEOIngestor(
        STACClient("https://stac.example.invalid", SinglePageTransport({})),
        sink,
        max_workers=2,
    )

    await ingestor.ingest(
        [
            STACItem(
                item["id"],
                "sentinel-2-l2a",
                "fixture://scene",
                item["properties"],
                item,
            )
            for item in items
        ]
    )

    assert sink.maximum <= 2
