# Agent continuity guide

## Purpose

`kvarken-eo-pipeline` is a thesis repository for hybrid Earth Observation data ingestion, validation, and spatial processing in the Kvarken Space Center context. The code should remain useful for reproducible research and operationally realistic experiments.

## Canonical commands

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest
python -m ruff check .
python -m ruff format --check .
python -m kvarken_eo --demo
```

## Architecture rules

- Keep application code under `src/kvarken_eo/` and tests under `tests/`.
- Model external data at the boundary with typed dataclasses; validate before transforms.
- Keep I/O async and injectable. Production adapters must implement the same protocol as test fakes.
- Keep provider-specific parsing in adapters; pass validated, transport-neutral records to sinks and transforms.
- Store raw payloads with a SHA-256 checksum and append-only provenance metadata.
- Bound concurrent provider work with `ConcurrentEOIngestor(max_workers=...)`; never create unbounded tasks.
- Use `FileProvenanceSink.store_async()` for async pipelines so manifest appends are serialized and filesystem I/O leaves the event loop.
- Keep retries explicit and bounded. Never retry malformed payloads; retry only transient timeout and rate-limit failures.
- Keep geospatial transforms deterministic and separate from transport concerns.
- Use `KVARKEN_REGION_BBOX` and EPSG:4326 spatial helpers for regional filtering; reject unknown CRS instead of silently reprojecting.
- Use `SpatialCatalog` for persistent scene metadata; query with bbox pre-filtering before exact polygon checks and keep writes transactionally committed.
- Run `python -m kvarken_eo verify-health` after storage changes; keep retention pruning explicit and provenance deletion dry-run by default.
- Use `ingest_with_metrics()` when batch telemetry is needed; preserve `ingest()` compatibility and keep metrics dependency-free.
- Use `benchmark-report` for reproducible offline reports and run pre-commit hooks before handoff.
- Keep quality profiling metadata-only; use catalog `max_cloud_cover` and `required_assets` filters before any raw-payload work.
- Use `CDSETokenProvider` for OAuth2 credentials and inject transports in tests; never put tokens in fixtures or reports.
- Keep raster access range-based and dependency-free; validate aligned red/NIR arrays before calculating NDVI.
- Keep the educational HTTP API read-only and backed by `SpatialCatalog`; validate query parameters at the boundary.
- Treat `docs/experiments/` as durable thesis artifacts generated only from offline, checked-in fixtures.
- Prefer standard library types and small modules over framework abstractions.
- Update `docs/PROJECT_STATUS.md` at each weekly checkpoint and record durable decisions in `docs/ARCHITECTURE.md`.

## Async and rate-limit safety

- Use bounded concurrency; do not create unbounded tasks from provider responses.
- Apply exponential backoff with a cap and honor a provider's retry delay when available.
- Set explicit network timeouts and propagate terminal errors with context.
- Do not mutate shared state from concurrent tasks without an explicit ownership boundary.
- Treat HTTP 429 and timeouts as transient; treat corrupted payloads and schema failures as permanent input errors.

## Milestone checklist

- [x] Repository identity and Python packaging established
- [x] Typed mock ingestion vertical slice implemented
- [x] Timeout, rate-limit, and corrupted-payload tests added
- [x] Public STAC adapter, offline fixtures, and provenance sink implemented
- [x] STAC-to-EOScene transformation and bounded concurrent ingestion implemented
- [x] Kvarken spatial filtering and offline 429 throughput harness implemented
- [x] Persistent SQLite spatial catalog and 1,200-scene query benchmark implemented
- [x] Catalog/provenance retention maintenance and offline health CLI implemented
- [x] Matrix CI workflow and structured ingestion telemetry implemented
- [x] Deterministic experiment reports, benchmark CLI, and pre-commit hooks implemented
- [x] Scene quality profiler, catalog quality filters, and report quality summaries implemented
- [x] CDSE OAuth2 adapter, raster range fetch/NDVI slice, and educational catalog API implemented
- [x] Thesis baseline experiment artifacts generated and documentation freeze recorded
- [x] Developer and agent commands documented
- [x] Add persistent raw/staged storage with provenance metadata
- [ ] Add spatial index and representative Sentinel-1/Sentinel-2 fixtures
- [ ] Benchmark bounded concurrent ingestion and document findings

## Change checklist

Before handing off work:

1. Add or update tests for changed behavior.
2. Run `python -m pytest`, `python -m ruff check .`, and `python -m ruff format --check .`.
3. Update status and roadmap documents when scope or milestones change.
4. Confirm no secrets, raw data, caches, or generated artifacts are staged.
