# Kvarken EO Pipeline

Production-minded research scaffold for hybrid Earth Observation (EO) data ingestion and processing in the Kvarken Space Center context. The repository favors small, typed, async-aware components that can be extended during weekly research checkpoints without losing continuity.

## Prerequisites

- Python 3.11 or newer
- Git

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Verify

```powershell
python -m pytest
python -m ruff check .
python -m ruff format --check .
```

The package includes a dependency-free STAC client built on the Python standard library. Its transport is injectable, so tests and research runs can remain offline. The initial demo still uses an in-memory EO source:

```powershell
python -m kvarken_eo --demo
```

## Repository map

- `src/kvarken_eo/` - ingestion contracts, STAC adapter, validation, provenance sink, and CLI demo
- `tests/` - unit tests, offline STAC fixtures, and provenance verification
- `docs/` - goals, architecture, current status, and roadmap
- `AGENTS.md` - continuity and contribution rules for people and coding agents

## Development conventions

Keep source code under `src/`, add a focused test for every behavior change, and update the relevant document in `docs/` when a milestone or architectural decision changes. Do not commit credentials, raw datasets, generated artifacts, or local environment files.

### Concurrent ingestion

`ConcurrentEOIngestor` transforms and persists STAC items with a bounded `max_workers` semaphore. The default is four workers; use a lower value when a provider has stricter rate limits:

```python
from pathlib import Path

from kvarken_eo import ConcurrentEOIngestor, FileProvenanceSink, STACClient

pipeline = ConcurrentEOIngestor(
    STACClient("https://earth-search.aws.element84.com/v1"),
    FileProvenanceSink(Path("data/staged")),
    max_workers=2,
)
results = await pipeline.search_and_ingest(collections=("sentinel-2-l2a",))
```

The provenance sink serializes JSONL appends with an async lock and performs filesystem work in a worker thread, keeping the event loop responsive.

### Persistent scene catalog

`SpatialCatalog` stores normalized scene metadata in a dependency-free SQLite database. Bbox, platform, and acquisition-time columns are indexed; ROI queries use SQL bbox pre-filtering followed by exact polygon intersection:

```python
from kvarken_eo import SpatialCatalog

with SpatialCatalog("data/scenes.sqlite") as catalog:
    catalog.index_scene(scene)
    matches = catalog.query_scenes(
        roi=(20.5, 62.8, 22.5, 63.8),
        platform="sentinel-2",
    )
```

Re-indexing a `scene_id` updates its metadata atomically. `ConcurrentEOIngestor` accepts `catalog=...` to index each successfully persisted scene.

### Kvarken spatial filtering

Spatial helpers use dependency-free WGS84 axis-aligned bounds and polygon edge tests:

```python
from kvarken_eo import KVARKEN_REGION_BBOX, scene_intersects_roi

if scene_intersects_roi(scene, KVARKEN_REGION_BBOX):
    print("scene overlaps the Kvarken archipelago study region")
```

The default `KVARKEN_REGION_BBOX` is `(20.5, 62.8, 22.5, 63.8)` in EPSG:4326. Boundary-touching scenes count as intersecting; non-WGS84 scenes are rejected rather than silently reprojected.
