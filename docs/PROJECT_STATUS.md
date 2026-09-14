# Project status

## 2026-09-14 - STAC and provenance milestone

Status: green provider milestone.

- Added a dependency-free async STAC `/search` adapter with pagination and bounded timeout/rate-limit retries.
- Added representative Sentinel-2 STAC JSON fixtures under `tests/fixtures/`.
- Added a filesystem provenance sink with canonical raw payloads, SHA-256 checksums, and append-only JSONL audit records.
- Added offline tests for pagination, retries, schema validation, and provenance persistence.
- Added STAC-to-`EOScene` normalization for geometry/bbox, EPSG, assets, acquisition time, and optional cloud cover.
- Added semaphore-bounded concurrent transformation and persistence with async-locked provenance writes.
- Added concurrency tests verifying worker bounds and complete, parseable audit records.

## 2026-09-14 - Bootstrap

Status: green foundation.

- Created `kvarken-eo-pipeline` package layout and developer documentation.
- Implemented an offline async mock fetcher with typed scene metadata.
- Added schema validation and bounded retry handling for timeouts and rate limits.
- Added tests for the happy path and timeout, rate-limit, and corrupted-payload failures.
- No external credentials or datasets are required.

## Next checkpoint

Evaluate persistent storage throughput and provider rate-limit behavior under bounded concurrent ingestion.
