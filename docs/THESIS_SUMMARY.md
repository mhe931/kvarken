# Kvarken EO Pipeline Thesis Summary

## Review status

This is a working thesis draft. Professor Arslan must review the draft and plan before final
submission. The [supervisor review plan](SUPERVISOR_REVIEW_PLAN.md) records the proposed
completion sequence and the evaluation questions awaiting his feedback.

## Research focus

This repository evaluates a reproducible, hybrid Earth Observation data pipeline for the
Kvarken Space Center context. The work focuses on provider-boundary validation, bounded
asynchronous ingestion, provenance, spatial metadata queries, and lightweight analytical
processing without requiring heavyweight geospatial dependencies.

## Architecture and data flow

1. A public STAC or authenticated CDSE adapter queries scene metadata through an injectable
   transport.
2. Boundary validation converts provider payloads into typed `STACItem` and `EOScene` records.
3. `ConcurrentEOIngestor` applies an explicit semaphore limit while transforming scenes, writing
   content-addressed raw payloads, and indexing normalized metadata.
4. `SpatialCatalog` persists queryable metadata in SQLite with platform/time and bounding-box
   indexes, followed by exact ROI checks.
5. Quality profiling evaluates cloud cover, geometry, and asset completeness from catalog
   metadata.
6. Reports export structured JSON and publication-ready Markdown. The educational HTTP layer
   exposes read-only catalog queries, while the raster slice supports HTTP ranges and NDVI over
   aligned numerical bands.

## Methods

The implementation is standard-library-only at runtime. Network behavior is injectable and
offline fixtures are checked in, allowing deterministic tests for pagination, OAuth2 refresh,
rate limits, timeouts, malformed payloads, bounded concurrency, SQLite contention, and report
generation. Raw payloads are hashed with SHA-256 and accompanied by append-only provenance
records.

## Empirical evidence

The frozen offline baseline contains a 256-scene synthetic run at concurrency 8 in
[`docs/experiments/experiment_report.json`](experiments/experiment_report.json). It records
throughput, elapsed time, payload footprint, catalog size, spatial query latency, cloud-cover
quality, asset completeness, and a recovery-ratio field. Because failures and retries are zero
in this run, that ratio does not demonstrate recovery from a provider outage. Environment-aware live runs write dated
`experiment_report_live_YYYYMMDD` artifacts without overwriting that baseline.

The dated `experiment_report_live_20260915.json` explicitly records `offline-fallback` mode.
Its metadata comes from the offline fixture, and its spectral window is synthetic. It is not
evidence of authenticated CDSE access or measurements on downloaded satellite imagery.

## Validation status

The current repository includes offline tests for:

- typed scene and STAC schema validation;
- bounded ingestion and provenance writes;
- multi-threaded SQLite catalog upserts and concurrent reads;
- OAuth2 token expiration, rate-limit recovery, timeout propagation, and invalid responses;
- catalog quality filters, spatial intersections, raster ranges, NDVI, HTTP queries, and reports.

The canonical verification commands are:

```powershell
python -m pytest
python -m ruff check .
python -m ruff format --check .
python -m kvarken_eo verify-health
```

The earlier thesis-summary checkpoint recorded 53 offline tests and clean quality gates. That
is a historical checkpoint, not a current test count. The 5 October 2026 documentation
checkpoint verified 63 passing offline tests, Ruff lint and formatting, and `verify-health`. Live
CDSE evidence remains environment-dependent and must be added as a dated artifact when valid
credentials are available.

## Limitations and next research steps

The raster slice deliberately avoids decoding full GeoTIFF structures; it validates range
transport and numerical NDVI behavior. The live-provider path is not exercised in CI. Future
work should add authenticated CDSE observations, representative raster windows, and comparative
benchmarks while retaining the frozen offline baseline for regression analysis.
