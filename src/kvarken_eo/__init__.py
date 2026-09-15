"""Foundations for the Kvarken Earth Observation pipeline."""

from .api import create_catalog_server
from .catalog import SpatialCatalog
from .cdse import CDSEClient, CDSETokenProvider, OAuthToken
from .concurrent import ConcurrentEOIngestor, ConcurrentIngestionResult, IngestionMetrics
from .ingestion import AsyncIngestor, IngestionResult, RetryPolicy
from .models import EOScene, PayloadValidationError
from .provenance import FileProvenanceSink, ProvenanceRecord
from .quality import SceneQualityProfile, profile_scene_quality
from .raster import (
    AffineGridTransform,
    DownsampleBenchmark,
    RasterAssetFetcher,
    benchmark_downsample,
    calculate_ndvi,
    downsample_band,
)
from .reports import generate_experiment_report
from .runner import (
    CDSESettings,
    prune_live_experiment_artifacts,
    resolve_cdse_settings,
    run_live_experiment,
)
from .spatial import KVARKEN_REGION_BBOX, bbox_intersects, scene_intersects_roi
from .stac import STACClient, STACItem
from .transform import transform_stac_to_scene

__all__ = [
    "AsyncIngestor",
    "create_catalog_server",
    "CDSEClient",
    "CDSESettings",
    "CDSETokenProvider",
    "ConcurrentEOIngestor",
    "ConcurrentIngestionResult",
    "IngestionMetrics",
    "KVARKEN_REGION_BBOX",
    "EOScene",
    "FileProvenanceSink",
    "IngestionResult",
    "PayloadValidationError",
    "OAuthToken",
    "ProvenanceRecord",
    "RasterAssetFetcher",
    "AffineGridTransform",
    "DownsampleBenchmark",
    "benchmark_downsample",
    "generate_experiment_report",
    "SceneQualityProfile",
    "profile_scene_quality",
    "prune_live_experiment_artifacts",
    "resolve_cdse_settings",
    "RetryPolicy",
    "SpatialCatalog",
    "STACClient",
    "STACItem",
    "bbox_intersects",
    "calculate_ndvi",
    "downsample_band",
    "scene_intersects_roi",
    "run_live_experiment",
    "transform_stac_to_scene",
]
