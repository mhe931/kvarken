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
- Added Python 3.11/3.12 GitHub Actions CI and structured batch ingestion metrics for counts, elapsed time, throughput, failures, retries, and payload bytes.
- Added deterministic JSON/Markdown experiment reporting, offline `benchmark-report` CLI generation, and pre-commit Ruff/whitespace hooks.
- Added dependency-free scene quality profiles, catalog cloud/asset filters, and quality distributions in experiment reports.
- Added CDSE OAuth2 client-credentials token caching/refresh with injectable offline transports.
- Added dependency-free HTTP range asset fetching and aligned-band NDVI calculation.
- Added a read-only standard-library catalog query API with health and JSON scene endpoints.
- Generated the thesis baseline under `docs/experiments/` using 256 synthetic scenes and concurrency 8.
- Added an environment-aware live experiment runner with CDSE credential resolution, offline fallback, network telemetry, response distributions, and immutable dated artifacts.
- Added automated OAuth recovery coverage for token expiry, rate limits, invalid responses, and timeouts, plus a dry-run-by-default live artifact retention utility.
- Added multi-threaded SQLite contention and high-volume ingestion worker-limit stress tests.
- Added `docs/THESIS_SUMMARY.md` as the academic architecture, methods, evidence, and limitations index.
- Added SQLite WAL mixed-reader/writer throughput profiling and post-contention durability regression coverage.

## 2026-09-15 - Thesis manuscript scaffold

Status: manuscript structure prepared for academic drafting.

- Added `thesis/main.tex`, abstract, five modular chapters, and `references.bib`.
- Populated introductory research questions, background standards, architecture/data-flow design,
  implementation methods, and the exact 256-scene empirical baseline table.
- Kept the manuscript independent of source code and frozen experiment artifacts; no runtime
  behavior or baseline data was modified.
- Added a GitHub Actions manuscript workflow that installs TeX Live, runs the
  `pdflatex`/BibTeX compilation sequence, and uploads `main.pdf` as a workflow artifact for
  thesis-scoped pushes and pull requests.

## 2026-09-15 - Release readiness audit

Status: released `0.1.0`; documentation and continuity audit complete.

- Reconciled roadmap and agent checklists with all implemented provider, raster, API, telemetry,
  quality, concurrency, WAL, and thesis artifact capabilities.
- Confirmed 53 offline tests, Ruff quality gates, and `verify-health` as the release validation
  baseline.
- Confirmed the frozen experiment report is never targeted by live artifact pruning.
- Annotated tag `v0.1.0` and the official GitHub Release identify the certified baseline.

## 2026-09-14 - Bootstrap

Status: green foundation.

- Created `kvarken-eo-pipeline` package layout and developer documentation.
- Implemented an offline async mock fetcher with typed scene metadata.
- Added schema validation and bounded retry handling for timeouts and rate limits.
- Added tests for the happy path and timeout, rate-limit, and corrupted-payload failures.
- No external credentials or datasets are required.

## Thesis freeze checkpoint

Status: baseline implementation and offline empirical artifact freeze complete. The checked-in report records the current 256-scene synthetic run; future live CDSE experiments must add a new dated artifact rather than overwrite this baseline.
