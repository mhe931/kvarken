# Project status

## 2026-10-22 - Expanded thesis revision and PR in progress

- Added a referenced comparison of CDSE, Google Earth Engine, Microsoft Planetary Computer,
  CREODIAS, openEO, Pangeo and Open Data Cube, with brief positioning of the additional
  services requested in the revision brief.
- Added a nine-stage CSC student workflow diagram and evidence table. The table distinguishes
  the one demonstrated five-record metadata replay from offline/local tests and steps that
  remain proposed or not tested; it does not claim CSC raster processing or student outcomes.
- Expanded the alphabetical abbreviation list and checked first use in the manuscript. The
  abstract is 442 words and contains no specific numeric research results.
- Static source checks passed for the requested platform coverage, workflow stages, four-layer
  methodology, abbreviation entries, and citation/reference-key consistency.
- A fresh source audit also verified 63 unique, alphabetized abbreviations, 60 resolved
  bibliography keys, 18 resolved cross-references, the 442-word abstract, and the completed
  bearer-header example. `git diff --check` passed.
- Current-source PR CI passed on Python 3.11 and 3.12: each base test job reported 83 passed
  and 3 skipped; Ruff lint and format checks, offline health checks, and both optional
  science/document jobs passed. XeLaTeX/Biber compilation also passed and reported an
  82-page CI PDF. That artifact has not been visually inspected and is not an
  official-template export or PDF/A/accessibility validation.
- Local tests and builds remain unavailable: `python` resolves to a Microsoft Store stub,
  and the local TeX/PDF toolchain is absent. GitHub Actions run 67 produced a 69-page PDF
  for an earlier source revision and is not evidence for this branch.
- Edge Personal opened the existing Google Doc and displayed a saved-to-Drive status and
  recent author edit attribution. After refresh, its content area rendered blank. No text
  or graphics were edited, and revised content or professor access has not been verified.
  The Google Slides presentations were not updated or verified.
- Current-source official-template DOCX, PDF/A validation, accessibility review, final page
  counts, and a current supervisor-response pagination pass remain open.
- No new satellite acquisition, CSC deployment, email, Turnitin upload, or Osuva submission
  was performed. A pull request for this expanded source revision is open, and its current
  CI checks pass; merge, document export, and Google Drive synchronization remain outstanding.

### Previous source checkpoint

The earlier 22 October source checkpoint passed 91 tests, Ruff lint and formatting, offline
`verify-health`, both documented CLI help commands, a source-level citation/reference-label
check, and the thesis-build workflow. Those results predate the platform-comparison and
student-workflow edits above and are not current-source verification.

## 2026-10-19 - Actual-data application; external acceptance gates open

- Recovered the nine-chapter manuscript from existing PR #22 without discarding its work.
- Executed real Sentinel-1 RTC / Sentinel-2 L2A / WorldCover processing on the local CPU.
- Corrected optical tile ownership, native class purity, land screening, single-class
  block reporting and item-specific provenance after an independent computational review.
- Held-out proxy agreement is 88.00%, balanced agreement 88.26%, ice precision 23.53%.
  This is diagnostic evaluation, not validated total sea-ice extent.
- Published small checksummed evidence under [research/20261019](research/20261019/README.md);
  raw windows remain ignored. Frozen synthetic artifacts are unchanged.
- Expanded local suite: 90 passing tests with optional science/document dependencies.
- CSC project **2021696** was verified with cPouta enabled and 30,000 Cloud BUs. The
  five-scene metadata/provenance/catalog/API workload actually executed remotely at
  17:29:42 UTC, exit zero; retrieved hashes and exact local/remote validation passed.
  See [CSC evidence](research/20261019/csc_execution_evidence.json).
- Both temporary VMs, floating IP and SSH ingress rule were released after retrieval;
  the project and automatic network/router remain. No public API was exposed.
- Existing Google Doc synchronization, personal author review and university approvals
  remain open. No emails or university submissions were made.
- Revised the manuscript and produced official-styled review exports. Local rendering does
  not establish author acceptance, supervisor acceptance or university submission readiness.

The [delivery report](THESIS_DELIVERY_REPORT_20261019.md) and
[current review plan](SUPERVISOR_REVIEW_PLAN.md) supersede the schedule below.
23 October is the user's urgent working deadline, not a publicly verified universal deadline.

## 2026-10-05 - Supervisor review and completion planning

Status: working thesis draft; supervisor review pending.

The manuscript and software baseline are available for review, but thesis acceptance and final
submission readiness have not been established. Professor Arslan has asked to review the draft
plan and thesis status before accepting a final manuscript. The next step is to send the status
and draft work plan as an email attachment and revise the thesis after his written feedback.

The frozen report covers 256 synthetic scenes. The dated 20260915 report uses
`offline-fallback` mode and an `offline-fixture` provider; its filename does not indicate an
authenticated CDSE experiment. These results support the tested implementation behavior, but
do not establish live-provider performance, operational deployment, or full raster decoding.

Verification on this checkpoint: 63 offline tests passed; Ruff lint and formatting checks,
`verify-health`, and whitespace diff checks passed. No runtime code or frozen experiment
artifacts changed. Earlier test counts below are historical checkpoints.

See [the supervisor review plan](SUPERVISOR_REVIEW_PLAN.md) for the proposed October–December
2026 sequence, outstanding scope questions, and document workflow. The schedule is a proposal
for review, not a confirmed University deadline or an assurance of graduation.


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
- Added Chapter 6, `Conclusion and Future Work`, answering all four research questions and
  defining follow-on work for continuous CDSE ingestion, raster operations, distributed catalogs,
  and operational Kvarken deployment.
- Added formal frontmatter acknowledgements and an operational abbreviation table, plus table of
  contents, figures, and tables lists to the manuscript.
- Certified the complete manuscript through GitHub Actions run
  [34957031561](https://github.com/mhe931/kvarken/actions/runs/34957031561): TeX Live installation,
  four-pass LaTeX/BibTeX compilation, and `kvarken-thesis` PDF artifact upload all succeeded.
  The downloaded `main.pdf` was verified locally as a non-empty 280,592-byte PDF.

## 2026-09-15 - Multiscale raster milestone

Status: green offline spatial-processing milestone.

- Added brightness-preserving block-average downsampling with correctly normalized partial edge
  blocks.
- Added affine local-pixel to EPSG:4326 bounding-box alignment and inverse coordinate mapping.
- Added multiband scene reduction and throughput/peak-memory benchmark helpers.
- Added focused raster transform and benchmark regression coverage; the offline suite now passes
  60 tests.
- Updated architecture and thesis implementation documentation with the mathematical contract and
  dependency-free limitations.

## 2026-09-15 - Live spectral-window telemetry

Status: green offline-fallback telemetry milestone.

- Integrated calibrated B04/B08 window extraction, factor-two reduction, and NDVI evaluation into
  `live-experiment`.
- Generated immutable `experiment_report_live_20260915.json` and Markdown artifacts without
  modifying the frozen 256-scene baseline.
- Recorded 142.551675 windows/sec, 14,136 traced peak-memory bytes, and sample NDVI 0.423131 for
  the 16x16-to-8x8 synthetic window.
- The repository now passes 63 offline tests.

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
