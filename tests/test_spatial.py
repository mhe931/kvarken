from datetime import UTC, datetime

import pytest

from kvarken_eo.models import EOScene, PayloadValidationError
from kvarken_eo.spatial import (
    KVARKEN_REGION_BBOX,
    bbox_intersects,
    polygon_intersects_bbox,
    scene_intersects_roi,
)


def scene(bbox, footprint=None, epsg=4326):
    return EOScene(
        "scene",
        "sentinel-2",
        datetime(2026, 1, 1, tzinfo=UTC),
        0,
        footprint
        or (
            (bbox[0], bbox[1]),
            (bbox[2], bbox[1]),
            (bbox[2], bbox[3]),
            (bbox[0], bbox[3]),
        ),
        bbox,
        epsg,
        {},
    )


def test_kvarken_boundary_touch_counts_as_intersection():
    assert bbox_intersects((20.5, 62.8, 20.6, 62.9), KVARKEN_REGION_BBOX)
    assert scene_intersects_roi(scene((22.5, 63.7, 22.6, 63.8)))


def test_contained_and_disjoint_scenes():
    assert scene_intersects_roi(scene((21.0, 63.0, 21.1, 63.1)))
    assert not scene_intersects_roi(scene((18.0, 60.0, 19.0, 61.0)))


def test_polygon_crossing_roi_without_vertices_inside_is_detected():
    polygon = ((20.0, 63.2), (23.0, 63.2), (23.0, 63.3), (20.0, 63.3))
    assert polygon_intersects_bbox(polygon, KVARKEN_REGION_BBOX)


@pytest.mark.parametrize(
    "value",
    [
        (1, 2, 0, 3),
        (1, 2, 3),
    ],
)
def test_invalid_bboxes_raise(value):
    with pytest.raises(PayloadValidationError):
        bbox_intersects(value, KVARKEN_REGION_BBOX)


def test_non_wgs84_scene_is_rejected():
    with pytest.raises(PayloadValidationError, match="WGS84"):
        scene_intersects_roi(scene((21, 63, 21.1, 63.1), epsg=32635))
