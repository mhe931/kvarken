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
- Added dependency-free Kvarken EPSG:4326 bbox/polygon filtering with boundary and invalid-geometry tests.
- Added an offline throughput harness with injected latency, burst 429 responses, jittered retry policy, and manifest completeness checks.
- Added persistent SQLite scene catalog with bbox/platform/time indexes, idempotent upserts, ROI exact filtering, and synthetic 1,200-scene query benchmarking.
- Added locked catalog retention pruning, integrity/WAL checkpoint/vacuum maintenance, provenance orphan/age inspection with dry-run-safe deletion, and an offline `verify-health` CLI smoke test.

## 2026-09-14 - Bootstrap

Status: green foundation.

- Created `kvarken-eo-pipeline` package layout and developer documentation.
- Implemented an offline async mock fetcher with typed scene metadata.
- Added schema validation and bounded retry handling for timeouts and rate limits.
- Added tests for the happy path and timeout, rate-limit, and corrupted-payload failures.
- No external credentials or datasets are required.

## Next checkpoint

Evaluate SQLite maintenance throughput and retention policies against larger research catalogs.
