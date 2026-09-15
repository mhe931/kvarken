"""Foundations for the Kvarken Earth Observation pipeline."""

from .catalog import SpatialCatalog
from .cdse import CDSEClient, CDSETokenProvider, OAuthToken
from .concurrent import ConcurrentEOIngestor, ConcurrentIngestionResult, IngestionMetrics
from .ingestion import AsyncIngestor, IngestionResult, RetryPolicy
from .models import EOScene, PayloadValidationError
from .provenance import FileProvenanceSink, ProvenanceRecord
from .quality import SceneQualityProfile, profile_scene_quality
from .raster import RasterAssetFetcher, calculate_ndvi
from .reports import generate_experiment_report
from .spatial import KVARKEN_REGION_BBOX, bbox_intersects, scene_intersects_roi
from .stac import STACClient, STACItem
from .transform import transform_stac_to_scene

__all__ = [
    "AsyncIngestor",
    "CDSEClient",
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
    "generate_experiment_report",
    "SceneQualityProfile",
    "profile_scene_quality",
    "RetryPolicy",
    "SpatialCatalog",
    "STACClient",
    "STACItem",
    "bbox_intersects",
    "calculate_ndvi",
    "scene_intersects_roi",
    "transform_stac_to_scene",
]
