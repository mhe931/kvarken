# Kvarken EO Pipeline Thesis Summary

## Review status

**22 October update:** the canonical manuscript was revised against the supplied review
brief. Current-source compilation and saved Google Docs synchronization remain unverified;
the browser redirected to Google sign-in. The [review-response matrix](THESIS_REVIEW_RESPONSE_20261022.md)
maps each item to source sections and evidence.

Actual Sentinel-1/independent Sentinel-2 pixels were processed locally on 19 October. The
[research record](research/20261019/README.md) reports the method, selective proxy evaluation
and low positive precision. The candidate map is not validated total ice extent. The
[delivery report](THESIS_DELIVERY_REPORT_20261019.md) preserves the earlier execution and
export evidence. The historical baseline description below remains applicable to the core only.

This is a working thesis draft. Professor Arslan must review the draft and plan before final
submission. The [supervisor review plan](SUPERVISOR_REVIEW_PLAN.md) records the proposed
completion sequence and the evaluation questions awaiting his feedback.

## Research focus

This repository develops an in-house hybrid Earth Observation data infrastructure to support
research and teaching within Kvarken Space Center and the University of Vaasa. It focuses on
provider-boundary validation, bounded active concurrency, provenance, spatial metadata
queries, and a lightweight metadata baseline. Optional scientific dependencies support local
raster analysis.

## Architecture and data flow

1. STAC and the implemented CDSE OAuth2/STAC metadata interface use injectable transports.
   CDSE tests use offline fakes; live CDSE metadata access is not confirmed.
2. Boundary validation converts provider payloads into typed `STACItem` and `EOScene` records.
3. `ConcurrentEOIngestor` applies an explicit semaphore limit to active work while transforming scenes, writing
   content-addressed raw payloads, and indexing normalized metadata.
4. `SpatialCatalog` persists queryable metadata in SQLite with platform/time and bounding-box
   indexes, followed by exact ROI checks.
5. Quality profiling evaluates cloud cover, geometry, and asset completeness from catalog
   metadata.
6. Reports export structured JSON and publication-ready Markdown. The educational HTTP layer
   exposes read-only catalog queries, while the raster slice supports HTTP ranges and NDVI over
   aligned numerical bands.

## Methods

The core implementation is standard-library-only at runtime. Network behavior is injectable and
offline fixtures are checked in, allowing deterministic tests for pagination, OAuth2 refresh,
rate limits, timeouts, malformed payloads, bounded active concurrency, SQLite contention, and
report generation. Raw payloads are hashed with SHA-256 and accompanied by append-only
provenance records. The batch call still schedules one coroutine per input item; it does not
bound scheduling memory for arbitrarily large batches.

## Empirical evidence

The frozen offline baseline contains a 256-scene synthetic run at concurrency 8 in
[`docs/experiments/experiment_report.json`](experiments/experiment_report.json). It records
throughput, elapsed time, payload footprint, catalog size, spatial query latency, cloud-cover
quality, asset completeness, and a recovery-ratio field. Because failures and retries are zero
in this run, its legacy value of 1.0 is a reporting convention and recovery is not measured
(N/A). Fault-injection tests provide the recovery evidence. Environment-aware runs write dated
`experiment_report_live_YYYYMMDD` artifacts without overwriting that baseline.

The dated `experiment_report_live_20260915.json` explicitly records `offline-fallback` mode.
Its metadata comes from the offline fixture, and its spectral window is synthetic. It is not
evidence of authenticated CDSE access or measurements on downloaded satellite imagery.

## Validation status

The current repository includes tests for:

- typed scene and STAC schema validation;
- bounded active ingestion and provenance writes;
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

The 19 October evidence record reports 90 passing tests with optional science/document
dependencies. The 22 October source revision passed 91 tests, Ruff lint/format checks and
the offline health check. Live CDSE evidence remains unverified and must be added as a dated
artifact only after an authorized reproducible run.

## Limitations and next research steps

The generic raster-range slice and the optional local scientific case study do not implement
CDSE pixel downloads. The real case uses Sentinel observations hosted/distributed through
Microsoft Planetary Computer and upstream CATALYST Sentinel-1 RTC. CSC project 2021696
executed five authentic metadata records through provenance, SQLite, regional queries and a
loopback API; raster classification ran locally. Current student exercises include fixture
metadata work, source validation, provenance inspection, catalog queries, read-only API use,
and local real-data processing. Learning outcomes were not evaluated. Future work includes
live CDSE access, larger raster workflows, bounded streaming scheduling and educational
evaluation while preserving the frozen offline baseline.
