"""Dependency-free WGS84 spatial filtering helpers."""

from collections.abc import Sequence

from .models import EOScene, PayloadValidationError

Coordinate = tuple[float, float]
BBox = tuple[float, float, float, float]
KVARKEN_REGION_BBOX: BBox = (20.5, 62.8, 22.5, 63.8)


def validate_bbox(bbox: Sequence[float]) -> BBox:
    if len(bbox) != 4:
        raise PayloadValidationError("bbox must contain four coordinates")
    values = tuple(float(value) for value in bbox)
    min_x, min_y, max_x, max_y = values
    if min_x > max_x or min_y > max_y:
        raise PayloadValidationError("bbox minimums cannot exceed maximums")
    return values


def bbox_intersects(left: Sequence[float], right: Sequence[float]) -> bool:
    """Return true when two closed axis-aligned boxes overlap or touch."""
    a_min_x, a_min_y, a_max_x, a_max_y = validate_bbox(left)
    b_min_x, b_min_y, b_max_x, b_max_y = validate_bbox(right)
    return not (a_max_x < b_min_x or b_max_x < a_min_x or a_max_y < b_min_y or b_max_y < a_min_y)


def polygon_intersects_bbox(polygon: Sequence[Coordinate], bbox: Sequence[float]) -> bool:
    """Test polygon/box overlap using vertices, corners, and edge crossings."""
    if len(polygon) < 3:
        raise PayloadValidationError("polygon must contain at least three points")
    region = validate_bbox(bbox)
    if any(_point_in_bbox(point, region) for point in polygon):
        return True
    corners = (
        (region[0], region[1]),
        (region[2], region[1]),
        (region[2], region[3]),
        (region[0], region[3]),
    )
    if any(_point_in_polygon(corner, polygon) for corner in corners):
        return True
    return any(
        _segments_intersect(start, end, edge_start, edge_end)
        for start, end in zip(polygon, tuple(polygon[1:]) + (polygon[0],), strict=True)
        for edge_start, edge_end in zip(corners, corners[1:] + (corners[0],), strict=True)
    )


def scene_intersects_roi(scene: EOScene, roi: Sequence[float] = KVARKEN_REGION_BBOX) -> bool:
    if scene.epsg != 4326:
        raise PayloadValidationError("scene must use WGS84 EPSG:4326 for regional filtering")
    if scene.bbox is not None and bbox_intersects(scene.bbox, roi):
        return True
    return polygon_intersects_bbox(scene.footprint, roi)


def _point_in_bbox(point: Coordinate, bbox: BBox) -> bool:
    return bbox[0] <= point[0] <= bbox[2] and bbox[1] <= point[1] <= bbox[3]


def _point_in_polygon(point: Coordinate, polygon: Sequence[Coordinate]) -> bool:
    x, y = point
    inside = False
    for start, end in zip(polygon, tuple(polygon[1:]) + (polygon[0],), strict=True):
        if (start[1] > y) != (end[1] > y):
            crossing_x = (end[0] - start[0]) * (y - start[1]) / (end[1] - start[1]) + start[0]
            if x < crossing_x:
                inside = not inside
    return inside


def _segments_intersect(a: Coordinate, b: Coordinate, c: Coordinate, d: Coordinate) -> bool:
    def orientation(first: Coordinate, second: Coordinate, third: Coordinate) -> float:
        return (second[0] - first[0]) * (third[1] - first[1]) - (second[1] - first[1]) * (
            third[0] - first[0]
        )

    def on_segment(first: Coordinate, second: Coordinate, point: Coordinate) -> bool:
        return min(first[0], second[0]) <= point[0] <= max(first[0], second[0]) and min(
            first[1], second[1]
        ) <= point[1] <= max(first[1], second[1])

    values = (
        orientation(a, b, c),
        orientation(a, b, d),
        orientation(c, d, a),
        orientation(c, d, b),
    )
    if values[0] == 0 and on_segment(a, b, c):
        return True
    if values[1] == 0 and on_segment(a, b, d):
        return True
    if values[2] == 0 and on_segment(c, d, a):
        return True
    if values[3] == 0 and on_segment(c, d, b):
        return True
    return (values[0] > 0) != (values[1] > 0) and (values[2] > 0) != (values[3] > 0)
