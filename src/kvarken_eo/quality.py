"""Dependency-free scene metadata quality profiling."""

from collections.abc import Sequence
from dataclasses import dataclass

from .models import EOScene


@dataclass(frozen=True, slots=True)
class SceneQualityProfile:
    """Quality flags and normalized scores for one scene."""

    scene_id: str
    is_usable: bool
    missing_assets: tuple[str, ...]
    geometry_valid: bool
    cloud_risk_score: float
    quality_score: float


def profile_scene_quality(
    scene: EOScene,
    required_assets: Sequence[str] | None = None,
    *,
    max_cloud_cover: float = 20.0,
) -> SceneQualityProfile:
    required = tuple(required_assets or ())
    missing = tuple(asset for asset in required if asset not in scene.assets)
    geometry_valid = (
        scene.epsg == 4326
        and len(scene.footprint) >= 3
        and all(len(point) == 2 for point in scene.footprint)
    )
    cloud_risk = round(min(1.0, max(0.0, scene.cloud_cover / 100.0)), 6)
    cloud_ok = scene.cloud_cover <= max_cloud_cover
    is_usable = geometry_valid and cloud_ok and not missing
    score = (
        (1.0 - cloud_risk) * 0.6
        + (1.0 if geometry_valid else 0.0) * 0.2
        + (1.0 if not missing else 0.0) * 0.2
    )
    return SceneQualityProfile(
        scene.scene_id,
        is_usable,
        missing,
        geometry_valid,
        cloud_risk,
        round(score, 6),
    )
