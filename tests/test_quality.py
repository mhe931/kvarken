from datetime import UTC, datetime

import pytest

from kvarken_eo import EOScene, SpatialCatalog, profile_scene_quality


def make_scene(scene_id: str, cloud_cover: float, assets: dict[str, str]) -> EOScene:
    return EOScene(
        scene_id,
        "sentinel-2",
        datetime(2026, 1, 1, tzinfo=UTC),
        cloud_cover,
        ((21, 63), (21.1, 63), (21.1, 63.1)),
        (21, 63, 21.1, 63.1),
        4326,
        assets,
    )


def test_quality_profile_scores_cloud_and_assets():
    profile = profile_scene_quality(
        make_scene("usable", 10, {"red": "fixture://red"}),
        required_assets=("red", "nir"),
    )

    assert profile.is_usable is False
    assert profile.missing_assets == ("nir",)
    assert profile.geometry_valid is True
    assert profile.cloud_risk_score == 0.1
    assert 0 < profile.quality_score < 1


def test_quality_profile_rejects_cloud_and_invalid_crs():
    scene = make_scene("cloudy", 80, {"red": "fixture://red"})
    invalid = EOScene(
        scene.scene_id,
        scene.platform,
        scene.acquired_at,
        scene.cloud_cover,
        scene.footprint,
        scene.bbox,
        32635,
        scene.assets,
    )

    profile = profile_scene_quality(invalid, required_assets=("red",))

    assert profile.is_usable is False
    assert profile.geometry_valid is False
    assert profile.cloud_risk_score == 0.8


def test_catalog_quality_filters_use_stored_metadata(tmp_path):
    with SpatialCatalog(tmp_path / "catalog.sqlite") as catalog:
        catalog.index_scene(
            make_scene("clear", 5, {"red": "fixture://red", "nir": "fixture://nir"})
        )
        catalog.index_scene(make_scene("cloudy", 60, {"red": "fixture://red"}))

        results = catalog.query_scenes(max_cloud_cover=20, required_assets=("red", "nir"))

        assert [scene.scene_id for scene in results] == ["clear"]


def test_catalog_rejects_invalid_cloud_filter(tmp_path):
    with SpatialCatalog(tmp_path / "catalog.sqlite") as catalog:
        with pytest.raises(ValueError, match="max_cloud_cover"):
            catalog.query_scenes(max_cloud_cover=101)
