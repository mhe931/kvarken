# Roadmap

## Foundation (complete)

- Typed source and scene contracts
- Offline mock provider
- Explicit transient failure retries
- Tests and continuity documentation

## Provider integration (complete)

- Implemented one public STAC catalog adapter with pagination and retry handling.
- Added representative Sentinel-2 metadata fixtures and offline tests.
- Added CDSE OAuth2 client-credentials authentication with environment-based configuration and
  offline fallback seams.
- Records source URLs, collection identifiers, retry attempts, checksums, and acquisition
  timestamps through provenance metadata.

## Provenance and processing (baseline complete)

- Implemented filesystem raw-payload storage and append-only provenance audit records.
- Added COG-like HTTP range access and dependency-free NDVI over aligned numerical bands.
- Added deterministic geometry, bbox, EPSG:4326, cloud-cover, and asset validation.
- Added fixture-based unit and smoke tests for transforms, catalog queries, and the educational API.

## Evaluation and operations (baseline complete)

- Measured bounded-ingestion throughput, retries, payload footprint, catalog query latency, and
  quality distributions in deterministic reports.
- Added structured ingestion metrics, WAL contention profiling, durability regression coverage,
  and environment-aware live-run telemetry.
- Documented reproducibility and thesis experiment procedures in `THESIS_SUMMARY.md`.

## Thesis baseline freeze (complete)

- CDSE OAuth2 client-credentials adapter with offline fallback seams.
- COG-like byte-range asset fetcher and dependency-free NDVI slice.
- Read-only educational HTTP catalog service.
- Checked-in 256-scene benchmark JSON/Markdown artifacts under `docs/experiments/`.

Future work should add live-provider observations as new immutable experiment records and retain the offline baseline for regression comparison.

## Release follow-up

- Published annotated `v0.1.0` tag and official GitHub Release for the certified thesis baseline.
- Add authenticated CDSE observations and representative raster windows as dated artifacts.
- Compare live-provider results with the frozen offline baseline without overwriting it.
