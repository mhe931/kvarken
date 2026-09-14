# Project status

## 2026-09-14 - STAC and provenance milestone

Status: green provider milestone.

- Added a dependency-free async STAC `/search` adapter with pagination and bounded timeout/rate-limit retries.
- Added representative Sentinel-2 STAC JSON fixtures under `tests/fixtures/`.
- Added a filesystem provenance sink with canonical raw payloads, SHA-256 checksums, and append-only JSONL audit records.
- Added offline tests for pagination, retries, schema validation, and provenance persistence.

## 2026-09-14 - Bootstrap

Status: green foundation.

- Created `kvarken-eo-pipeline` package layout and developer documentation.
- Implemented an offline async mock fetcher with typed scene metadata.
- Added schema validation and bounded retry handling for timeouts and rate limits.
- Added tests for the happy path and timeout, rate-limit, and corrupted-payload failures.
- No external credentials or datasets are required.

## Next checkpoint

Add a provider-specific scene-to-`EOScene` transformation and evaluate persistent storage behavior under bounded concurrent ingestion.
