"""Transform validated STAC GeoJSON items into transport-neutral scenes."""

from collections.abc import Mapping
from datetime import datetime

from .models import EOScene, PayloadValidationError


def transform_stac_to_scene(stac_item: Mapping[str, object]) -> EOScene:
    """Normalize one STAC item, using conservative defaults for optional metadata."""
    item_id = stac_item.get("id")
    properties = stac_item.get("properties")
    collection = stac_item.get("collection")
    geometry = stac_item.get("geometry")
    if not isinstance(item_id, str) or not item_id:
        raise PayloadValidationError("STAC item id must be a non-empty string")
    if not isinstance(properties, Mapping):
        raise PayloadValidationError("STAC item properties must be an object")
    if not isinstance(collection, str) or not collection:
        raise PayloadValidationError("STAC item collection must be a non-empty string")

    acquired_at = properties.get("datetime")
    if not isinstance(acquired_at, str):
        raise PayloadValidationError("STAC item requires an ISO datetime")
    try:
        datetime.fromisoformat(acquired_at.replace("Z", "+00:00"))
    except ValueError as error:
        raise PayloadValidationError("STAC item datetime is invalid") from error

    platform = properties.get("platform") or _platform_from_collection(collection)
    if not isinstance(platform, str) or not platform:
        raise PayloadValidationError("STAC item platform must be a non-empty string")
    cloud_cover = properties.get("eo:cloud_cover", 0.0)
    try:
        cloud_cover = float(cloud_cover)
    except (TypeError, ValueError) as error:
        raise PayloadValidationError("STAC cloud cover must be numeric") from error

    raw_bbox = stac_item.get("bbox")
    bbox = _bbox(raw_bbox)
    footprint = _footprint(geometry, bbox)
    raw_epsg = properties.get("proj:epsg", 4326)
    try:
        epsg = int(raw_epsg)
    except (TypeError, ValueError) as error:
        raise PayloadValidationError("STAC EPSG must be an integer") from error

    raw_assets = stac_item.get("assets", {})
    if not isinstance(raw_assets, Mapping):
        raise PayloadValidationError("STAC assets must be an object")
    assets = {
        name: asset["href"]
        for name, asset in raw_assets.items()
        if isinstance(name, str)
        and isinstance(asset, Mapping)
        and isinstance(asset.get("href"), str)
    }
    return EOScene.from_payload(
        {
            "scene_id": item_id,
            "platform": platform,
            "acquired_at": acquired_at,
            "cloud_cover": cloud_cover,
            "footprint": footprint,
            "bbox": bbox,
            "epsg": epsg,
            "assets": assets,
        }
    )


def _platform_from_collection(collection: str) -> str:
    normalized = collection.lower().replace("_", "-")
    if "landsat" in normalized:
        return "landsat-8/9"
    if "sentinel-1" in normalized or "sentinel1" in normalized:
        return "sentinel-1"
    if "sentinel-2" in normalized or "sentinel2" in normalized:
        return "sentinel-2"
    return collection


def _bbox(raw_bbox: object) -> tuple[float, float, float, float] | None:
    if raw_bbox is None:
        return None
    try:
        values = tuple(float(value) for value in raw_bbox)  # type: ignore[union-attr]
    except (TypeError, ValueError) as error:
        raise PayloadValidationError("STAC bbox must contain numeric coordinates") from error
    if len(values) != 4:
        raise PayloadValidationError("STAC bbox must contain four coordinates")
    return values  # type: ignore[return-value]


def _footprint(
    geometry: object, bbox: tuple[float, float, float, float] | None
) -> tuple[tuple[float, float], ...]:
    if isinstance(geometry, Mapping) and geometry.get("type") == "Polygon":
        coordinates = geometry.get("coordinates")
        if isinstance(coordinates, list) and coordinates and isinstance(coordinates[0], list):
            ring = coordinates[0]
            points = tuple(
                (float(point[0]), float(point[1]))
                for point in ring
                if isinstance(point, (list, tuple)) and len(point) >= 2
            )
            if len(points) >= 3:
                return points
    if bbox is not None:
        min_x, min_y, max_x, max_y = bbox
        return ((min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y))
    raise PayloadValidationError("STAC item requires polygon geometry or bbox")
