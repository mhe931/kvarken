# Thesis delivery and blocker report: 19 October 2026

## A. Executive decision

**Substantial actual implementation completed; the thesis is not submission-ready.**

Real Sentinel-1 radar, independent Sentinel-2 optical observations and a WorldCover mask
have been acquired, processed and evaluated. The full manuscript now connects the
infrastructure to that actual application. However:

- Positive ice precision is low and most candidate ice area has no optical label.
  This is diagnostic proxy evaluation, **not validated total sea-ice extent**.
- Actual CSC metadata/provenance/catalog/API execution is now verified; raster analysis
  remains local and the remote replay does not improve classifier accuracy.
- The existing shared native Google Doc has not been synchronized or remotely verified.
- Independent PDF/A-3A validation now passes for the locally remediated candidate.
  Personal author/accessibility review, supervisor acceptance, reviewer confirmation,
  Turnitin authorization and Osuva authorization remain open. Full PDF/UA-1 conformance
  is not claimed; its identification requirement remains unsatisfied.

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

## F. CSC: actual remote workload executed and independently verified

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
| Allocation verified before launch | **30,000 Cloud BUs**, 0 used, 100% remaining |
| OpenStack quota verified | 8 instances, 8 vCPUs, 32.2 GB RAM, 2 floating IPs, 10 volumes |

The agent did not accept declarations or submit the application. Creation and activation
were verified afterward at https://my.csc.fi/projects/2021696. The service displays
1 January 2027 as its boundary although the application requested 31 December; no precise
expiry hour is inferred. This allocation is not proof of OpenStack resource quota.

An initial cPouta authorization denial was followed by successful authenticated access
after the supported sign-in route. The selected project was verified as `project_2021696`.
The precise earlier entitlement/propagation cause is not established. No agent accepted
personal security enrollment/terms. No support email was sent.

The actual execution VM was **8d3f5911-360b-48fb-83a6-115a95d8bd5b**, OpenStack project
**a1842d0445334e65afc3a2be05c5ac80**. It used `standard.tiny`: **one vCPU, 1,000 MB RAM,
80 GB ephemeral disk**, Ubuntu **24.04.5 LTS**, Python **3.12.3**, clean Git revision
`0a009885e07f1bf25f2e1960ceb3f9ce3e4ac5c1`.

Two restricted SSH attempts to an initial VM timed out. Instead of broadening access,
a second VM executed the existing workload through supported cloud-init user data.
The authenticated console recorded actual execution and supplied a compressed evidence archive:

| Actual remote measurement | Value |
|---|---:|
| Runner start UTC, 19 October | 17:29:42.844271 |
| Runner completion UTC | 17:29:43.815320 |
| Runner elapsed | 0.971050 s |
| Ingestion-only elapsed / derived rate | 0.199499 s / 25.062840 items/s |
| Scenes / canonical payload bytes | 5 / 68,286 |
| Failures / retries / command exit status | 0 / 0 / 0 |
| Locally reverified output / source files | 8 / 20 |

Exact catalog, regional-query and loopback-API scene identities, health response and five
provenance records equal the local validation. Linux input matches the reviewed Git blob.
Windows checkout CRLF versus Linux LF explains the raw input-file checksum difference;
parsed metadata is identical. Timestamp-bearing outputs need not be byte-identical.
No remote raster processing, fresh provider benchmark or cloud speedup is claimed.

Archive SHA-256: `c12807b646e95916540826166c02febecdec39d85034a167d90282c21b3f85df`.
See [sanitized remote run](research/20261019/csc_pipeline_run.json) and
[control-plane/evidence summary](research/20261019/csc_execution_evidence.json).
Original console, archive, extracted logs/environment/results and exact bootstrap script
are retained in ignored `outputs/thesis_delivery_20261019/`. The generic runner's provider
field remains `not-verified`; separate authenticated control-plane identity establishes CSC.

**Cleanup verified:** both session-created VMs deleted, floating IP released, temporary SSH
rule removed. The dashboard shows 0 instances/vCPUs/RAM, 0 floating IPs, 0 volumes and the
original four security rules. The project and automatic network/router remain allocated.
No public API was exposed. Cloud BU accounting may update later; no zero-cost claim is made.
Allas/Roihu and password/application-credential API access were unnecessary. The isolated
OpenStack CLI 10.4.0 remains installed locally; no cookies or tokens were extracted.

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
counts, majority comparison, area support, failure interpretation and verified CSC
metadata-deployment methods/results. Raster classification remains explicitly local.
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

### Latest final-verification package

- [Current DOCX with scientific figure descriptions](../outputs/thesis_verified_review_20261019/Thesis_Review_20261019.docx).
- [Current locally remediated PDF/A submission candidate, 71 pages](../outputs/thesis_verified_review_20261019/Thesis_Submission_Candidate_20261019.pdf).
- [Final content/layout/metadata audit](../outputs/thesis_verified_review_20261019/final_verification.json).
- [Independent PDF/A-3A report](../outputs/thesis_verified_review_20261019/pdfa3a_validation.xml).
- [Independent PDF/UA-1 report](../outputs/thesis_verified_review_20261019/pdfua1_validation.xml).

**veraPDF 1.30.3 ran locally**, not an online upload: PDF/A-3A passed **155 rules /
753,556 checks, zero failures**. This is independent validation, not inference from XMP.
The separate PDF/UA-1 check passed **105 rules / 272,819 checks** but failed **one
identification requirement**; full PDF/UA conformance must not be asserted. Human review
of reading order, equations/tables, figure-description adequacy, keyboard navigation and
screen-reader use remains necessary. A conformance identifier was not added merely to
make the checker green.

The source exporter now gives all five scientific maps meaningful alternative text
without changing their measured results or visible captions. Word hyperlink screen tips
removed most annotation failures; nine figure/table page-reference links were then given
their complete actual field labels, and annotated pages were assigned structure-based
tab order. The local remediation audit records each changed annotation. Original exports
are preserved. Every candidate page was rendered and is **pixel- and text-identical** to
the previously inspected 71-page review PDF. All six original image byte sequences,
all paragraphs and all table text match the canonical DOCX export. Author/title metadata
and the university template are unchanged.
The PR review identified incorrect colour names in the first alternative descriptions.
They were corrected against the actual plotting source: pale-cyan snow ice, blue water,
grey missing/unlabelled areas, white exclusions and red disagreement. Expanded regression
checks failed against the previous exporter and passed after correction; the latest
linked files and validator reports include the corrected descriptions.

| Latest final-verification artifact | SHA-256 |
|---|---|
| DOCX | `71274e55c2fedf331639bfb6853d39f8fa0148b66a4c4df9a568236bafee0685` |
| Remediated PDF/A candidate | `97554ba83eb62922326ae6a11afe03d5583b813877c20679943decb7de8721aa` |

An independent AI scientific/source audit recalculated the unchanged precision, baseline,
confusion counts, areas and temporal offset, and reverified 20 source files, 22 scientific
outputs, 33 acquisition windows and 12 native-mask inputs. No acquisition, classification
or CSC deployment was repeated. The annual-retrospective-mask caveat is already explicit
in Chapter 8; it is not an omitted limitation. This audit is not human scientific approval.

### Preserved earlier CSC-integrated exports

- [CSC-integrated official-template DOCX](../outputs/thesis_csc_review_20261019_final/Thesis_Review_20261019.docx).
- [CSC-integrated Word-rendered review PDF](../outputs/thesis_csc_review_20261019_final/Thesis_Review_20261019.pdf).
- [LaTeX source build](../thesis/main.pdf), generated locally, not committed.
- [Scientific figures/manifests](research/20261019/README.md).
- [Build/export instructions](../thesis/README.md).

Calibri, official logo, 3 cm margins, continuous Arabic pages, chapter hierarchy, APA bibliography,
native Word page/contents fields and separate maps were implemented. The official June 2025
DOTX and August 2026 guidelines were inspected. Word 16.0 rendered the actual DOCX; a requested
PDF/A export option is **not independently validated conformance**. Personal final accessibility,
pagination and university-format review are still required.

The earlier pre-CSC Word/LaTeX review PDFs had **71/64 pages**. The CSC-integrated
review exports have **71/65 pages** after correcting abstract and conclusion overflow.
Their latest measured page counts and hashes are recorded in
[the CSC document audit](../outputs/thesis_csc_review_20261019_final/csc_document_audit.json).
Their layout engines paginate differently. All pages
were rendered to images; contact sheets and critical pages were inspected. Both abstracts
fit one page. The Word contents/page fields were actually updated, the five figure and four
table captions were checked, and a decimal-truncation defect in the figure list was fixed
with a regression test. No unresolved Word field/citation placeholder was found.
The pre-CSC [document audit](../outputs/thesis_delivery_20261019/document_audit.json)
is retained as historical evidence, not the identity of the new export.

| Current review artifact | SHA-256 |
|---|---|
| DOCX | `6c72c1f7db8c439bc68e7695783b5cd273245eec31d5abc3e0ebe8945685c423` |
| Word-rendered PDF | `d645bb0b6786e5953d9e29af4fca5a7aaa7315a016a3913bcfd747f5ca654dcf` |
| LaTeX PDF | `891d337b0b4aec65c56b2874c0a39814c97637c4c58d848bd7bf33ee60a23d63` |

Official Osuva guidance also requires correct PDF title/author properties. Inspection
found a blank title; the exporter and LaTeX metadata were corrected, with an assertion
observed failing before the fix and passing afterward. Both final PDFs now contain the
main title (without subtitle) and author. Every final page was rendered and is
pixel-identical to the visually inspected layout. The Word PDF has a structure tree,
101 bookmarks and **PDF/A-3A identification**; this is not independent conformance or
accessibility validation. The LaTeX PDF has **no structure tree or PDF/A identification**
and must not be used directly as an approved accessible Osuva submission.

The existing native Google Doc ID, link and permissions were not changed:
https://docs.google.com/document/d/1oq5FtrWh4Yb3yd2NBtUS0OgNO2jtuDUMqzVz0085lEE/edit

**Final transfer verification:** the author reported a completed transfer. Nevertheless,
fresh authenticated TXT, DOCX and PDF exports from that exact ID still show **66,734
characters, 42 PDF pages and one image**, versus 71 pages and six images in the current
local manuscript. All requested numerical markers (23.53, 95.99, 2021696, 0.971050 and
17:29:42) are absent. Reload and a `cache: no-store` request with a unique query parameter
returned the same old content. Only one document tab was visible. The exports are retained
in `outputs/thesis_google_verification_20261019/`; no successful saved transfer is inferred.
The author was asked to check the exact document/tab or repeat the transfer from the
current DOCX, but the interaction reported the user unavailable. This is a confirmed
saved-content mismatch, not a renewed login/MFA request.

It was successfully reopened in authenticated editing mode on 19 October. A read-only,
same-origin plain-text export returned HTTP 200 and 66,734 characters, but contained neither
the current **23.53** precision nor **95.99** baseline values. A recheck after the CSC
export also found neither project **2021696** nor **0.971050** timing. It is therefore not verified
as synchronized. No content, sharing or document ID was changed. The canvas editor's
automation actions did not reliably operate, including after reload; no authorized Google
Docs/Drive API connector was found. A precise human-assisted rich-content transfer from
the CSC-integrated Word draft into the **same** native Doc was requested; the user was
unavailable. Remote re-export and verification are still required. Do not upload a replacement Word file
or create a new Doc as a workaround.
One further supported keyboard-focus route reached the document content iframe, but a
formatted Word clipboard paste did not change its saved export. The original Google
manuscript was backed up locally as `google_doc_before_sync.docx`. No successful mutation
is claimed. The next human action is to open the CSC-integrated DOCX in Word, copy its
entire body, select the entire existing Google Doc body, paste **with formatting**, and
wait for **Saved to Drive**. The agent must then re-export and verify actual content,
figures/tables, citations, AI disclosure and pagination; a successful paste alone is insufficient.
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
The completed CSC run has separate remote evidence; document synchronization and academic
approval are not implied by green software CI. Follow-up branch
`csc-thesis-completion-20261019` contains that actual evidence and manuscript integration;
its final Git/CI disposition is recorded in the generated delivery audit and final handoff.
The actual evidence/manuscript commit is `bc36bee1200d829eaed7a71295d420cdd3d6c7c1`.
[PR #23](https://github.com/mhe931/kvarken/pull/23) merged on 19 October at **18:00:07 UTC**,
after six latest-head checks passed and the newline-provenance review thread was resolved.
All five post-merge checks passed. Local and remote main were reverified at
`10f91d41a6b6e63b5c3f8435e375f1cdd76d2fa4`.
The source executed on CSC remains the earlier `0a009885...` revision, not this later
documentation merge. Only newly found accessibility corrections justify further Git work.

- [x] Authentic satellite input and actual processing.
- [x] Maps, source manifests, quantitative proxy comparison and honest limitations.
- [x] Existing pipeline integration and source-hashed local execution.
- [x] Full working-draft revision and local Word/PDF exports.
- [ ] Convincing total-extent validation, if required beyond this diagnostic case.
- [x] Actual authorized CSC run and independently verified remote evidence.
- [ ] Existing Google Doc synchronization/reopen verification.
- [ ] Personal author review and acceptance of every revised claim/reference/disclosure.
- [ ] Professor Arslan's scientific approval and reviewer confirmation.
- [x] Independent local PDF/A-3A validation of the remediated candidate.
- [ ] Human accessibility/reading-order review; full PDF/UA-1 conformance is not established.
- [ ] Authorized university submission.

## L. Unsent supervisor email and exact submission sequence

**Draft only; no email has been sent.** Attach the reviewed DOCX/PDF, not an old candidate.

**Subject:** Revised thesis for final review and Turnitin permission

Dear Professor Arslan,

Please find the revised thesis attached for your final review. Chapters 5 and 6 now
document actual Sentinel-1 processing, Sentinel-2 proxy comparison, maps and quantitative
evaluation, together with a verified CSC cPouta metadata-pipeline demonstration.

Ice precision against the selective optical proxy is 23.53%; the always-water baseline
has 95.99% ordinary agreement. I therefore do not present the candidate map as validated
total sea-ice extent. The CSC run demonstrates infrastructure portability, not improved
scientific accuracy. Substantial AI assistance is disclosed.

Please confirm whether this revision meets the practical-application requirement and
whether I may proceed with the programme's Turnitin submission. Please also confirm the
applicable deadline and the proposed reviewer, Cem Özcan, given the 23 October working
target. I will await your authorization before the controlled submission stages.

Däniel

### University sequence; approvals must precede each controlled step

1. Author verifies the revised work; resolve scientific and CSC evidence requirements.
2. Email Professor Arslan the working draft and receive corrections. Do not infer approval.
3. Obtain the supervisor's permission to use the programme's Moodle Turnitin submission.
4. Submit the agreed draft there; the supervisor reviews the actual similarity report.
   No score is currently available.
5. Obtain explicit permission for Osuva. Prepare the authorized accessible PDF/A and ensure
   it is substantively identical to the approved file. The current locally validated
   candidate is linked in Section I; no review-stage file is automatically authorized.
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

For the School of Technology and Innovations, the public Moodle course name is
**School of Technology & Innovations Master's Thesis** (also listed in Finnish).
Follow the supervisor's exact return-box/file instructions; do not guess an assignment
or upload format. Attach the current DOCX and PDF candidate for email review. Use only
the authorized final version for Turnitin/Osuva, not the old Google export, untagged LaTeX
PDF, historical delivery files or an unapproved subsequent edit. Confirm the final
graduation timetable through Education Services; 23 October is not independently verified
as this author's individual university deadline.

Official sources checked on 19 October:
[Master's thesis](https://www.uwasa.fi/en/students/masters-thesis),
[writing/plagiarism guidance](https://www.uwasa.fi/en/students/writing-guidelines-and-plagiarism-detection),
[Osuva](https://uva.libguides.com/responsible-thesis/osuva),
[graduation event](https://www.uwasa.fi/en/students/publiikki-graduation-event).


## H. Subsequent verified Google Docs update (19 October 2026, later review)

The unresolved Google Doc status in Sections A and the earlier dated handoff is a **historical record of the failed transfer**; it is preserved intentionally. After that report was written, the author requested a renewed academic audit and a direct update to the existing shared document.

On 19 October, the live exact Google Doc (`1oq5FtrWh4Yb3yd2NBtUS0OgNO2jtuDUMqzVz0085lEE`, tab `t.0`) was opened through the authenticated Google Docs connector. Its earlier stale body was replaced in place by a **supervisor-review rendition** of the current 71-page scientific manuscript, preserving the original file ID and supervisor editing permissions. The saved content was read back from Google Docs and verified to contain all five Sentinel research figures, the revised author name, case-study source identifiers, the 23.53% positive precision, the 95.99% baseline, actual CSC project 2021696 and its timings, and an explicit AI-use appendix covering both ChatGPT and Copilot. The Google export was reopened and visually checked for maps, headings and non-empty pages. Earlier inherited bullet formatting was corrected, scientific formulas and comparison summaries were made readable, and five figure image links were verified.

**Status change:** Google Docs synchronization of the research narrative is VERIFIED for the existing live document, unlike the earlier failed manual-transfer attempts. It is **not a certified layout-identical or archival submission file**. PDF-to-editable reconstruction can alter tables, equations, code blocks, hyphenation, contents pagination, alternative text and spacing. Its subsequent Google PDF export spans about 74 pages and is not claimed to meet PDF/A or full accessibility. The previously validated 71-page Word-generated PDF/A-3A is still the preferred supervisor review attachment and provisional archival candidate, subject to matching final author spelling, human scientific review, accessibility and supervisor approval. No Turnitin check, plagiarism score, AI-detector score, email, Osuva submission or academic approval has been performed by this update.
