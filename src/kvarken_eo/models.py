"""Typed models and boundary validation for EO scene metadata."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime


class PayloadValidationError(ValueError):
    """Raised when a provider payload cannot become a valid EO scene."""


@dataclass(frozen=True, slots=True)
class EOScene:
    """Minimal transport-neutral scene metadata used by downstream processing."""

    scene_id: str
    platform: str
    acquired_at: datetime
    cloud_cover: float
    footprint: tuple[tuple[float, float], ...]
    bbox: tuple[float, float, float, float] | None = None
    epsg: int = 4326
    assets: Mapping[str, str] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Mapping[str, object]) -> "EOScene":
        required = ("scene_id", "platform", "acquired_at", "cloud_cover", "footprint")
        missing = [key for key in required if key not in payload]
        if missing:
            raise PayloadValidationError(f"missing required fields: {', '.join(missing)}")

        try:
            scene_id = payload["scene_id"]
            platform = payload["platform"]
            acquired_at = datetime.fromisoformat(str(payload["acquired_at"]))
            cloud_cover = float(payload["cloud_cover"])
            raw_footprint = payload["footprint"]
            footprint = tuple(
                (float(point[0]), float(point[1]))
                for point in raw_footprint  # type: ignore[index]
            )
        except (TypeError, ValueError, IndexError, KeyError) as error:
            raise PayloadValidationError("payload contains invalid scene fields") from error

        if not isinstance(scene_id, str) or not scene_id.strip():
            raise PayloadValidationError("scene_id must be a non-empty string")
        if not isinstance(platform, str) or not platform.strip():
            raise PayloadValidationError("platform must be a non-empty string")
        if not 0 <= cloud_cover <= 100:
            raise PayloadValidationError("cloud_cover must be between 0 and 100")
        if len(footprint) < 3:
            raise PayloadValidationError("footprint must contain at least three points")

        raw_bbox = payload.get("bbox")
        bbox = None
        if raw_bbox is not None:
            try:
                bbox = tuple(float(value) for value in raw_bbox)
            except (TypeError, ValueError) as error:
                raise PayloadValidationError("bbox must contain numeric coordinates") from error
            if len(bbox) != 4:
                raise PayloadValidationError("bbox must contain four coordinates")
        raw_epsg = payload.get("epsg", 4326)
        try:
            epsg = int(raw_epsg)
        except (TypeError, ValueError) as error:
            raise PayloadValidationError("epsg must be an integer") from error
        raw_assets = payload.get("assets", {})
        if not isinstance(raw_assets, Mapping):
            raise PayloadValidationError("assets must be a mapping")
        assets = {}
        for name, href in raw_assets.items():
            if not isinstance(name, str) or not isinstance(href, str) or not href:
                raise PayloadValidationError("asset names and hrefs must be non-empty strings")
            assets[name] = href

        return cls(scene_id, platform, acquired_at, cloud_cover, footprint, bbox, epsg, assets)
