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
- `docs/THESIS_SUMMARY.md` - academic overview of methods, data flow, evidence, and limitations
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

### Maintenance and health verification

Catalog retention and SQLite maintenance are explicit:

```python
catalog.prune_older_than(cutoff)
catalog.vacuum()
sink.prune_raw_payloads(catalog, dry_run=True)  # inspect first
sink.prune_raw_payloads(catalog, dry_run=False)  # explicit deletion
```

Run the deterministic end-to-end smoke check without network access:

```powershell
python -m kvarken_eo verify-health
```

The command uses a temporary directory, ingests the checked-in STAC fixture, records provenance, indexes and queries the scene, checks retention, runs SQLite integrity/vacuum maintenance, and confirms no payloads are unexpectedly orphaned.

### CI and batch metrics

GitHub Actions runs Ruff, pytest, and the offline health check on pushes and pull requests targeting `main` for Python 3.11 and 3.12. No live provider calls are made.

`ConcurrentEOIngestor.ingest_with_metrics()` returns results plus an `IngestionMetrics` record containing scene count, elapsed seconds, throughput, failures, retry count, and canonical payload bytes. The legacy `ingest()` and `search_and_ingest()` methods remain list-returning APIs; their latest summary is available through `ingestor.last_metrics`.

Generate a reproducible synthetic benchmark report without network access:

```powershell
python -m kvarken_eo benchmark-report --output-dir reports --scenes-count 1000 --concurrency 8
```

This writes `experiment_report.json` and `experiment_report.md`. Local contributors can install the configured Ruff and whitespace hooks with `pre-commit install`.

### Scene quality profiling

Quality profiles are computed from stored scene metadata without opening raw payloads:

```python
from kvarken_eo import profile_scene_quality

profile = profile_scene_quality(
    scene,
    required_assets=("red", "nir"),
    max_cloud_cover=20,
)
```

Catalog queries can apply the same indexed metadata filters with `max_cloud_cover=20` and `required_assets=("red", "nir")`. Reports include usable-scene count/ratio, mean cloud cover, and asset completeness.

### Kvarken spatial filtering

Spatial helpers use dependency-free WGS84 axis-aligned bounds and polygon edge tests:

```python
from kvarken_eo import KVARKEN_REGION_BBOX, scene_intersects_roi

if scene_intersects_roi(scene, KVARKEN_REGION_BBOX):
    print("scene overlaps the Kvarken archipelago study region")
```

The default `KVARKEN_REGION_BBOX` is `(20.5, 62.8, 22.5, 63.8)` in EPSG:4326. Boundary-touching scenes count as intersecting; non-WGS84 scenes are rejected rather than silently reprojected.

### CDSE, raster, and educational API extensions

`CDSETokenProvider` performs OAuth2 client-credentials exchange with bounded, lock-protected token refresh. `CDSEClient` composes it with the existing STAC pagination and validation path; both token and STAC transports are injectable for offline tests. Credentials are supplied by the caller and are never stored in the repository.

`RasterAssetFetcher` performs inclusive HTTP byte-range requests for COG-like assets, while `calculate_ndvi()` computes dependency-free per-pixel NDVI values for aligned red/NIR arrays. Missing bands and shape mismatches fail explicitly.

`create_catalog_server()` exposes a small standard-library HTTP service with `/api/health` and `/api/scenes` endpoints. Scene queries accept `platform`, `start`, `end`, `max_cloud_cover`, and comma-separated `bbox` parameters and return JSON suitable for educational demonstrations.

### Thesis experiment artifacts

Generate the checked-in synthetic baseline with:

```powershell
python -m kvarken_eo benchmark-report --output-dir docs/experiments --scenes-count 256 --concurrency 8
```

The resulting [experiment_report.json](docs/experiments/experiment_report.json) and [experiment_report.md](docs/experiments/experiment_report.md) are durable, offline reproducibility records. Re-run the command for a new measurement and record the configuration in the corresponding thesis notebook.

Run the environment-aware live experiment command to query CDSE when all four credentials are
available, or to exercise the same pipeline against the checked-in fixture when they are absent:

```powershell
python -m kvarken_eo live-experiment --output-dir docs/experiments --scenes-count 25 --concurrency 4
```

The command reads `CDSE_TOKEN_URL`, `CDSE_CLIENT_ID`, `CDSE_CLIENT_SECRET`, and
`CDSE_STAC_URL`. It writes a dated `experiment_report_live_YYYYMMDD.json` plus Markdown companion,
records network round-trip latency and response distributions, and refuses to overwrite an artifact
from the same date. It never modifies the frozen `experiment_report.json`.

Inspect and prune dated live artifacts without touching the frozen baseline:

```powershell
python -m kvarken_eo prune-live-artifacts --output-dir docs/experiments --retention-days 30
python -m kvarken_eo prune-live-artifacts --output-dir docs/experiments --retention-days 30 --apply
```

The first command is a dry run. Only matching `experiment_report_live_YYYYMMDD` JSON/Markdown
pairs older than the retention window are selected; `experiment_report.json` is never a target.
