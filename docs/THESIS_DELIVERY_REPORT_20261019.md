# Thesis delivery and blocker report: 19 October 2026

## A. Executive decision

**Substantial actual implementation completed; the thesis is not submission-ready.**

Real Sentinel-1 radar, independent Sentinel-2 optical observations and a WorldCover mask
have been acquired, processed and evaluated. The full manuscript now connects the
infrastructure to that actual application. However:

- Positive ice precision is low and most candidate ice area has no optical label.
  This is diagnostic proxy evaluation, **not validated total sea-ice extent**.
- No actual CSC execution has been obtained.
- The existing shared native Google Doc has not been synchronized or remotely verified.
- Personal author review, supervisor acceptance, reviewer confirmation, final accessibility/
  PDF-A validation, Turnitin authorization and Osuva authorization remain open.

The user's **23 October 2026** working deadline is urgent but was not publicly verified as
an individual university assessment deadline. Confirm it immediately with Education Services.
No email, submission, approval, similarity score or graduation outcome is claimed.

## B. Recovery of previous work

The initial local and remote `main` were
`22c2b3edad279ed1d4316a4f773606b1d8617c46`, with a clean working tree.
Existing PR [#22](https://github.com/mhe931/kvarken/pull/22), head
`8730ba9a6bd59be65a2ed08f965bd8bdb35606d5`, contained the interrupted expanded manuscript.
Its prior LaTeX CI failed despite older prose claiming a clean build.

Its valid methodology, analysis, discussion and appendices were recovered into the existing
local feature branch `thesis-sentinel1-seaice-20261019`; they were not recreated independently.
The unescaped code identifier behind the known compilation failure was corrected.
Old “final” document links, page counts and unverified approval/AI-review wording were
replaced with truthful review status. Historical source remains available in Git.
No unrelated user work was reverted. Frozen synthetic/fallback artifacts were preserved.

## C. Actual inputs, access and rights

Exact IDs, acquisition metadata, unsigned source URLs and file hashes are in the
[research configuration and manifests](research/20261019/README.md).

| Role | Actual observation |
|---|---|
| SAR | Sentinel-1A IW GRDH VV/VH, ascending orbit 37230 / relative 58; 30 March 2021 16:06:12 UTC; Catalyst RTC |
| Optical reference sensor | Sentinel-2A L2A, 31 March 2021 10:00:21 UTC, R122, T34VER/T34VEQ/T34VDR/T34VDQ |
| Static land screening | ESA WorldCover 2021 v200, four 3-degree tiles |
| Domain | Eastern Kvarken rectangle 20.5–22.5°E / 62.8–63.8°N; 100 m EPSG:32634 grid |

Planetary Computer public STAC and officially issued anonymous read-only SAS tokens supplied
the observed raster bytes. An actual CDSE raster request returned 401; no authenticated
CDSE success is claimed. The RTC collection documentation states an account requirement,
but anonymous token issuance/range reads succeeded at the time. No access control was bypassed.

The [license record](research/20261019/source_licenses.json) preserves CC BY 4.0 for RTC and
WorldCover and the custom Copernicus Sentinel terms for optical data. The latter permit
adaptation/distribution with attribution; “proprietary” in STAC is not mislabelled CC BY.
Figures carry “Contains modified Copernicus Sentinel data 2021”.
Large raw windows/SAFE packages are not committed. Checksums identify retained reprojected
windows; a full-original SAFE checksum is explicitly unavailable.

## D. Implemented and executed method

The [scientific record](research/20261019/README.md) and Chapter 5 specify:

1. Sequential bounded COG range access, explicit timeouts, bounded throttling/timeout recovery,
   token caching and immutable interrupted-download reuse.
2. Provider-supplied calibration/RTC, common UTM alignment, positive linear-power averaging
   before decibel conversion, explicit nodata and reflectance scaling.
3. Native-resolution categorical fractions, largest connected pure-water component,
   300 m coastal erosion and common optical tile ownership.
4. Conservative SCL/reflectance water and snow-ice proxy labels with ≥99% native class purity.
5. Equal-prior VV/VH linear discriminant, 5% covariance shrinkage, fixed spatially separated
   10 km checkerboard interiors. No held-out tuning.
6. Candidate/reference/agreement maps, projected areas, complete per-block confusion metrics,
   majority baseline and decision-offset sensitivity.
7. Five captured actual scene records through the existing provenance, reopened catalog
   and loopback API checks, with original per-item source endpoints.

Noise treatment/RTC processor version are not independently verified. Wind and per-pixel
incidence effects are not corrected by this classifier. Official ice charts were not
treated as independent truth: their manual documents SAR inputs.

## E. Actual numerical findings and uncertainty

Authoritative machine-readable evidence:
[results JSON](research/20261019/results.json),
[metrics CSV](research/20261019/metrics.csv),
[sanitized local replay](research/20261019/local_pipeline_run.json).

| Quantity | Actual result |
|---|---:|
| Valid radar-water support | 5,952.79 km² |
| Held-out cells: water / snow ice | 84,846 / 3,546 |
| Confusion matrix: reference rows, candidate columns | `[[74641,10205],[406,3140]]` |
| Ordinary / balanced proxy agreement | 88.00% / 88.26% |
| Ice precision / recall / F1 | 23.53% / 88.55% / 37.18% |
| Always-water ordinary / balanced agreement | 95.99% / 50.00% |
| Candidate ice | 1,219.28 km² |
| Candidate ice without any proxy label | 795.91 km² (65.28%) |
| Same held-out support: reference / candidate positive area | 35.46 / 133.45 km² |
| Offset sensitivity −1 / 0 / +1 | 2,313.58 / 1,219.28 / 695.59 km² |

The majority baseline has higher ordinary agreement. The model detects many selected
snow-ice samples but has poor positive precision. No operational ice-extent claim is defensible.
The 17.90-hour mismatch, selective optical reference, spatial correlation, annual retrospective
mask and missing optical coverage limit inference. The offset range is not a confidence interval.
Projected cell areas are not ellipsoidal geodesic areas.

Final analysis started **16:06:54 UTC, 19 October 2026**; its **8.54 s** elapsed stage includes
calculations, publication maps and the local metadata/API replay, excluding acquisition
and native-mask retrieval. This is one local observation, not a stable performance benchmark.

## F. CSC: project created and funded; cPouta session/entitlement unresolved

The supported browser successfully reattached to authenticated MyCSC on 19 October.
No repeated CDP timeouts or new MyCSC login were needed. The earlier connection-level
failure is no longer reproducible. A new VS Code log session exists, but the exact cause
of the earlier timeout is not established; it is not evidence of a missing CSC account.

MyCSC initially showed **no projects**. Under the user's authorization, a Student Project
application was prepared through **Step 4: Confirmation** without accepting personal
declarations. A subsequent live inspection verified that it had been submitted and created:

| Field | Actual verified MyCSC value |
|---|---|
| Project number / Unix group | **2021696** / `project_2021696` |
| Name | Kvarken Earth Observation Thesis |
| Organization / role | University of Vaasa / author shown as project manager |
| Field | Natural sciences / 113 Computer and information sciences |
| Displayed lifetime | 19 October 2026 - 1 January 2027 |
| Service | cPouta **Enabled**, access granted 19 October 2026 |
| Actual allocated / used / remaining | **30,000 / 0 / 30,000 Cloud BUs (100%)** |
| OpenStack instance/vCPU/RAM/storage/network quotas | Not yet accessible/verified |

The agent did not accept declarations or submit the application. Creation and activation
were verified afterward at https://my.csc.fi/projects/2021696. The service displays
1 January 2027 as its boundary although the application requested 31 December; no precise
expiry hour is inferred. This allocation is not proof of OpenStack resource quota.

The actual cPouta page returned **"Login failed: You are not authorized for any projects
or domains."** New-project entitlement propagation is possible, not established.
A subsequent official Sign In / Haka / University of Vaasa attempt reached the actual
university sign-in screen. The author must complete that authentication/MFA privately;
the interaction request reported the user unavailable. If the denial persists, contact
`servicedesk@csc.fi` with project **2021696** and the exact error. No support email was sent.
Do not create a duplicate Student Project or request another MyCSC login.

The separate official cPouta API Access URL also requires service authentication. No VM,
network, SSH connection or remote measurements exist. No resources were created.
The official CLI route was checked: CSC documents `python-openstackclient` and
**API Access > Download OpenStack RC File v3**. It still requires an authorized project;
it cannot bypass the personal declarations. No endpoints, passwords or project IDs were
invented, and no browser cookies/tokens were extracted.

The [CSC procedure](CSC_DEMONSTRATION.md) contains a locally tested metadata replay command
and the exact missing remote evidence checklist. It is **prepared, not deployed**.
Allas and Roihu were not used. A stopped VM can still consume Cloud BUs; preserve outputs
and release only authorized temporary resources when no longer required.

## G. Local CPU/GPU and reproducible environment

Python 3.12.15 was restored in an isolated project environment after the PATH interpreter
proved to be a Store stub. The scientific run used NumPy 2.5.4, Rasterio 1.5.2,
GDAL 3.12.2, Matplotlib 3.11.2 and SciPy 1.18.1 on Windows CPU.

The NVIDIA T550 Laptop GPU has 4,096 MiB VRAM; driver 596.52 advertises CUDA compatibility
13.2. No installed CUDA runtime, GPU experiment, acceleration or neural training is claimed.
Small raster operations and a linear model did not justify GPU integration.

The metadata runtime retains no third-party dependencies. Science and document tools are
separate optional extras. Exact executed Python hashes are recorded because the working
tree was dirty; the old HEAD alone does not contain those modules. Private local hostname
is redacted from the published replay copy, with the original report hash preserved.

## H. Manuscript and scientific-integrity revision

[Canonical source](../thesis/main.tex) remains modular LaTeX. The approved title is unchanged.
Chapters 5–6 now contain actual acquisition, preprocessing, model/reference rules, maps,
counts, majority comparison, area support, failure interpretation and the missing CSC boundary.
Abstract, introduction/RQ5, background, methodology, analysis, discussion, conclusions,
abbreviations, AI disclosure and reproducibility appendix have also been revised.
Acknowledgements open with thanks to the author's parents.

The named “Daniel Academic Voice” skill was requested but is not installed. The user's stated
clear-English, direct, evidence-based voice constraints were applied manually; no skill
invocation or human acceptance is falsely claimed.

DOI metadata was checked for Drusch et al., Kovács et al., Small and Dierking; provider,
CSC and university documents support the corresponding claims. A mismatched Mahecha
reference/DOI was removed. The Dierking publisher abstract/metadata were accessible;
its full publisher PDF returned 403 and is not claimed to have been read.
No plagiarism/AI-detection/Turnitin score or independent human peer approval is invented.
The AI appendix explicitly discloses substantial assistance and pending personal author review.

## I. Documents and remote synchronization

- [Official-template DOCX](../outputs/thesis_delivery_20261019/Thesis_Review_20261019.docx).
- [Actual Word-rendered review PDF](../outputs/thesis_delivery_20261019/Thesis_Review_20261019.pdf).
- [LaTeX source build](../thesis/main.pdf), generated locally, not committed.
- [Scientific figures/manifests](research/20261019/README.md).
- [Build/export instructions](../thesis/README.md).

Calibri, official logo, 3 cm margins, continuous Arabic pages, chapter hierarchy, APA bibliography,
native Word page/contents fields and separate maps were implemented. The official June 2025
DOTX and August 2026 guidelines were inspected. Word 16.0 rendered the actual DOCX; a requested
PDF/A export option is **not independently validated conformance**. Personal final accessibility,
pagination and university-format review are still required.

The current Word-rendered review PDF has **71 pages**; the same canonical text compiled
with Tectonic/Biber has **64 pages**. Their layout engines paginate differently. All pages
were rendered to images; contact sheets and critical pages were inspected. Both abstracts
fit one page. The Word contents/page fields were actually updated, the five figure and four
table captions were checked, and a decimal-truncation defect in the figure list was fixed
with a regression test. No unresolved Word field/citation placeholder was found.
Checksums and measurable checks are retained in the local
[document audit](../outputs/thesis_delivery_20261019/document_audit.json).

The existing native Google Doc ID, link and permissions were not changed:
https://docs.google.com/document/d/1oq5FtrWh4Yb3yd2NBtUS0OgNO2jtuDUMqzVz0085lEE/edit

It was successfully reopened in authenticated editing mode on 19 October. A read-only,
same-origin plain-text export returned HTTP 200 and 66,734 characters, but contained neither
the current **23.53** precision nor **95.99** baseline values. It is therefore not verified
as synchronized. No content, sharing or document ID was changed. Synchronization is deferred
until the substantive CSC result is available, rather than insert an invented result or
replace the rich manuscript with unformatted text. Do not upload a replacement Word file
or create a new Doc as a workaround.
The old “Final Candidate” DOCX and Google Slides are historical, not revised deliverables.

## J. Verification and independent review

The expanded local environment passed **90 tests**, Ruff lint and format checks, the
storage health check and whitespace verification. A separate base-only environment passed
**74 tests with three optional modules skipped**, confirming offline operation without
science/document extras. The final audit independently verified all **33 original inputs,
12 native-mask inputs, 22 outputs and 20 executed-source hashes**, then recomputed the exact
confusion matrix and candidate/unsupported areas directly from saved rasters.
The [local science audit](../outputs/thesis_delivery_20261019/science_audit.json) records
these checks. Frozen baseline integrity passed.

Git disposition must be read with the generated delivery audit/final handoff, not inferred
from an earlier checkpoint. CI is configured for base Python 3.11/3.12 and optional scientific/
document paths; the manuscript smoke build uses XeLaTeX/Biber and Carlito on Linux.

The independent AI code/science review verified the initial 33 input hashes and reproduced
its confusion matrix, then identified six substantive defects/limitations. Corrections
cover common tile ownership, native land/purity masks, all single-class blocks, executed-source/
dependency evidence and item-specific provenance. Regression tests fail before the relevant
fixes and pass afterward. The reviewed stricter reference supersedes the initial result.
This is computational cross-checking, not human scientific approval.

All actual-data rasters remain ignored. Frozen reports are immutable. No credentials,
temporary SAS URLs, private keys, full satellite packages or generated thesis binaries
should enter the commit. The published local hostname is explicitly redacted.

## K. Git/GitHub disposition and remaining acceptance checklist

[PR #22](https://github.com/mhe931/kvarken/pull/22) was merged by `mhe931` on
19 October 2026 at **16:49:37 UTC**. Local and remote main were verified at
`0a009885e07f1bf25f2e1960ceb3f9ce3e4ac5c1`. All six pre-merge and five post-merge checks
passed; five review threads were resolved. Do not reopen or recreate that PR.
Remaining CSC execution and document synchronization are not implied by green software CI.

- [x] Authentic satellite input and actual processing.
- [x] Maps, source manifests, quantitative proxy comparison and honest limitations.
- [x] Existing pipeline integration and source-hashed local execution.
- [x] Full working-draft revision and local Word/PDF exports.
- [ ] Convincing total-extent validation, if required beyond this diagnostic case.
- [ ] Actual authorized CSC run and independently verified remote evidence.
- [ ] Existing Google Doc synchronization/reopen verification.
- [ ] Personal author review and acceptance of every revised claim/reference/disclosure.
- [ ] Professor Arslan's scientific approval and reviewer confirmation.
- [ ] Final accessibility/PDF-A validation and authorized university submission.

## L. Unsent supervisor email and exact submission sequence

**Draft only; no email has been sent.** Attach the reviewed DOCX/PDF, not an old candidate.

**Subject:** Revised Kvarken thesis: actual satellite experiment and CSC execution blocker

Dear Professor Arslan,

I have revised the thesis to include an actual Sentinel-1 application in eastern Kvarken.
Chapter 5 documents the observations, processing and infrastructure integration. Chapter 6
includes the input, candidate and independent Sentinel-2 comparison maps, quantitative
results and limitations.

The comparison reveals low precision among positive ice candidates, so I do not present
the map as validated total sea-ice extent. I would appreciate your priority feedback on
whether this diagnostic case meets the practical-application requirement or needs further
independent validation.

The CSC run has not yet been completed. Thesis project 2021696 has been created with cPouta
enabled and 30,000 Cloud BUs, but cPouta session/entitlement and instance-quota verification
remain unresolved. I have prepared the reproducible deployment procedure but have not presented
local measurements as CSC results. The repository evidence is available at
https://github.com/mhe931/kvarken/pull/22.

The revised working draft is attached for review, not submitted as an approved final thesis.
Please also confirm the individual deadline and the proposed reviewer, Cem Özcan, given
the 23 October working target for December graduation.

Däniel

### University sequence; approvals must precede each controlled step

1. Author verifies the revised work; resolve scientific and CSC evidence requirements.
2. Email Professor Arslan the working draft and receive corrections. Do not infer approval.
3. Obtain the supervisor's permission to use the programme's Moodle Turnitin submission.
4. Submit the agreed draft there; the supervisor reviews the actual similarity report.
   No score is currently available.
5. Obtain explicit permission for Osuva. Prepare the authorized accessible PDF/A and ensure
   it is substantively identical to the approved file.
6. Upload that file to Osuva and email the supervisor and the relevant Education Services.
   The public instructions identify `grades@uwasa.fi` for the School of Technology and Innovations;
   confirm current programme instructions before sending.
7. The assessment period starts after the Osuva upload and required emails; public guidance
   allows up to 30 days. Examiners and the Dean determine the grade.
8. Complete all degree requirements and the authenticated graduation application/timetable.
   The Jolla assessment timetable requires university login, so the individual 23 October
   deadline was not verified here.
9. Separately, the public graduation event is 18 December 2026 at 14:15, with event registration
   by 4 December. Ceremony dates do not guarantee individual thesis approval or graduation.

Official sources checked on 19 October:
[Master's thesis](https://www.uwasa.fi/en/students/masters-thesis),
[writing/plagiarism guidance](https://www.uwasa.fi/en/students/writing-guidelines-and-plagiarism-detection),
[Osuva](https://uva.libguides.com/responsible-thesis/osuva),
[graduation event](https://www.uwasa.fi/en/students/publiikki-graduation-event).
