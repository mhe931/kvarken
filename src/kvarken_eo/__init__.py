"""Foundations for the Kvarken Earth Observation pipeline."""

from .catalog import SpatialCatalog
from .concurrent import ConcurrentEOIngestor, ConcurrentIngestionResult, IngestionMetrics
from .ingestion import AsyncIngestor, IngestionResult, RetryPolicy
from .models import EOScene, PayloadValidationError
from .provenance import FileProvenanceSink, ProvenanceRecord
from .spatial import KVARKEN_REGION_BBOX, bbox_intersects, scene_intersects_roi
from .stac import STACClient, STACItem
from .transform import transform_stac_to_scene

__all__ = [
    "AsyncIngestor",
    "ConcurrentEOIngestor",
    "ConcurrentIngestionResult",
    "IngestionMetrics",
    "KVARKEN_REGION_BBOX",
    "EOScene",
    "FileProvenanceSink",
    "IngestionResult",
    "PayloadValidationError",
    "ProvenanceRecord",
    "RetryPolicy",
    "SpatialCatalog",
    "STACClient",
    "STACItem",
    "bbox_intersects",
    "scene_intersects_roi",
    "transform_stac_to_scene",
]
