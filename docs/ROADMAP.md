# Roadmap

## Deadline checkpoint: 19--23 October 2026

This supersedes the older proposed October--December sequence below. The user identifies
23 October as the submission working deadline; confirm the individual timetable with
Professor Arslan/Education Services rather than treating it as a public universal deadline.

- [x] Obtain and process authentic radar, optical and static-mask data.
- [x] Produce georeferenced maps, exact counts, selective independent-sensor comparison and manifests.
- [x] Diagnose low positive precision and unsupported extrapolation without inflating claims.
- [x] Revise the manuscript and prepare local review exports (the 19 October exports are historical).
- [x] Obtain authorized CSC project access and retain the actual remote metadata execution.
- [ ] Reopen and verify synchronization of the existing native Google Doc.
- [ ] Build and inspect the 22 October source revision; verify final pagination and independently
  validate any current PDF/A/accessibility output.
- [ ] Author examines the actual maps, code, references, AI disclosure and final pagination.
- [ ] Professor Arslan reviews the revised scientific scope and retained CSC metadata-execution evidence.
- [ ] Complete the authorized Turnitin/Osuva/assessment/graduation sequence.

The [review-response matrix](THESIS_REVIEW_RESPONSE_20261022.md) maps the supplied comments.
The [delivery report](THESIS_DELIVERY_REPORT_20261019.md) records historical evidence and gates.

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

- Measured bounded-active-concurrency throughput, retries, payload footprint, catalog query latency, and
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

## Historical 5 October proposal (superseded; not the current plan)

This sequence is for Professor Arslan's review. It does not confirm graduation or administrative
deadlines. See [the review plan](SUPERVISOR_REVIEW_PLAN.md) for the outstanding questions.

| Period | Proposed work | Evidence or review outcome |
|---|---|---|
| Early October | Send the status and draft work plan; request written feedback on scope and evaluation | Supervisor comments received by email |
| October | Revise research questions and methods; agree the minimum additional evaluation | Revised scope and an explicit experiment plan |
| November | Complete the agreed evaluation; revise results, discussion, and limitations | Dated evidence and a revised manuscript sent for review |
| Early December | Address feedback; check references, formatting, and graduation requirements | Corrected draft reviewed before final submission |
| Remaining December | Submit only after supervisor review and fulfil the confirmed University process | Submission and administrative steps, subject to deadlines |

Authenticated CDSE observations and representative raster windows are proposed additional
evidence. Whether they are essential to this thesis should be confirmed with the supervisor
before expanding the scope. Preserve the frozen offline baseline and keep new runs dated.
