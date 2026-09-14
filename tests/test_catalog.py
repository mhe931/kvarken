from datetime import UTC, datetime, timedelta

from kvarken_eo import EOScene, SpatialCatalog
from kvarken_eo.spatial import KVARKEN_REGION_BBOX


def make_scene(index: int, *, platform: str = "sentinel-2") -> EOScene:
    x = 20.0 + (index % 10) * 0.2
    y = 62.5 + (index % 10) * 0.1
    bbox = (x, y, x + 0.05, y + 0.05)
    return EOScene(
        f"scene-{index}",
        platform,
        datetime(2026, 1, 1, tzinfo=UTC) + timedelta(days=index),
        float(index % 20),
        ((x, y), (x + 0.05, y), (x + 0.05, y + 0.05), (x, y + 0.05)),
        bbox,
        4326,
        {"thumbnail": f"https://example.invalid/{index}.jpg"},
    )


def test_catalog_persists_and_reindexes_idempotently(tmp_path):
    path = tmp_path / "scenes.sqlite"
    with SpatialCatalog(path) as catalog:
        catalog.index_scene(make_scene(1))
        catalog.index_scene(make_scene(1, platform="landsat-8/9"))
        assert len(catalog.query_scenes()) == 1
        assert catalog.query_scenes()[0].platform == "landsat-8/9"
    with SpatialCatalog(path) as reopened:
        assert reopened.query_scenes()[0].scene_id == "scene-1"
        assert reopened.query_scenes()[0].assets["thumbnail"].endswith("1.jpg")


def test_catalog_filters_roi_platform_and_dates(tmp_path):
    with SpatialCatalog(tmp_path / "scenes.sqlite") as catalog:
        catalog.index_scenes([make_scene(index) for index in range(6)])
        catalog.index_scene(make_scene(100, platform="sentinel-1"))

        roi_results = catalog.query_scenes(roi=KVARKEN_REGION_BBOX)
        assert roi_results
        assert all(scene.platform == "sentinel-2" for scene in roi_results)
        filtered = catalog.query_scenes(
            platform="sentinel-1",
            start_time=datetime(2026, 4, 1, tzinfo=UTC),
        )
        assert [scene.scene_id for scene in filtered] == ["scene-100"]


def test_catalog_empty_query_is_empty(tmp_path):
    with SpatialCatalog(tmp_path / "scenes.sqlite") as catalog:
        assert catalog.query_scenes(platform="missing") == []


def test_catalog_retention_and_vacuum(tmp_path):
    path = tmp_path / "scenes.sqlite"
    with SpatialCatalog(path) as catalog:
        catalog.index_scenes([make_scene(0), make_scene(1)])
        removed = catalog.prune_older_than(datetime(2026, 1, 2, tzinfo=UTC))
        catalog.vacuum()
        assert removed == 1
        assert [scene.scene_id for scene in catalog.query_scenes()] == ["scene-1"]
