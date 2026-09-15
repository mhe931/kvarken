# Roadmap

## Foundation (complete)

- Typed source and scene contracts
- Offline mock provider
- Explicit transient failure retries
- Tests and continuity documentation

## Provider integration (complete)

- Implemented one public STAC catalog adapter with pagination and retry handling.
- Added representative Sentinel-2 metadata fixtures and offline tests.
- Add authentication through environment variables or managed identity only.
- Record request IDs, source URLs, and acquisition timestamps.

## Provenance and processing

- Implemented filesystem raw-payload storage and append-only provenance audit records.
- Add cloud-optimized raster metadata and spatial reference validation.
- Introduce deterministic tile/window transforms.
- Add small fixture-based integration tests.

## Evaluation and operations

- Measure throughput, retry behavior, and memory use under bounded concurrency.
- Add structured logging and metrics hooks.
- Document reproducibility and thesis experiment procedures.

## Thesis baseline freeze (complete)

- CDSE OAuth2 client-credentials adapter with offline fallback seams.
- COG-like byte-range asset fetcher and dependency-free NDVI slice.
- Read-only educational HTTP catalog service.
- Checked-in 256-scene benchmark JSON/Markdown artifacts under `docs/experiments/`.

Future work should add live-provider observations as new immutable experiment records and retain the offline baseline for regression comparison.
