# Source coverage and access report

**Prepared:** 26 October 2026  
**Deliverable:** *Kvarken Thesis: Learn the Science and Engineering* (`Kvarken_Thesis_Learn.md`, `.docx`, and `.pdf`)  
**Scope:** Source discovery, course access, thesis/repository coverage, evidence boundaries, and unresolved gaps.

## Executive finding

The textbook is a **new educational derivative**, not a revision verified against the original `Kvarken_theses_learn.docx`. That DOCX was not present in the worktree or the session files available to this run, so its complete contents, original figures, and 11-part sequence could not be read. The book therefore uses an explicitly new 11-lesson progression and must not be described as preserving unseen text.

The repository contains a modular thesis manuscript, software, tests, benchmark reports, and a dated real-data case-study record. These were used to ground the book. Both supplied Moodle URLs redirected to the University Haka login page in the available non-profile fetch. The authenticated Edge Personal window showed course-related tab titles, but it detected active user input when interaction was attempted. No course page, syllabus, lecture, presentation, reading, assignment, video, or supporting resource was inspected. No course-specific material or administrative requirements are claimed as incorporated.

## Moodle access record

| Requested source | Access evidence | Course identity and year | Materials inspected | Safe conclusion |
|---|---|---|---|---|
| `https://learn.uwasa.fi/course/section.php?id=51091` | Non-profile request redirected to `https://learn.uwasa.fi/login/index.php`, which displayed “Log in using Haka user account.” The authenticated Edge Personal window contained a tab titled “Foundations of Space Data and Earth Observation Systems (2026),” but the tab's URL/resource content could not be inspected because Edge reported active user input. | The section title, course code, current year, course identity, and relationship to this thesis are **unverified**. The visible tab title alone cannot be mapped to this URL. | None. | Course content cannot be cited or said to support any chapter. Do not infer syllabus or degree requirements. |
| `https://learn.uwasa.fi/course/view.php?id=5192` | Non-profile request redirected to the same Haka login page. No authenticated course page was read. | Course title, code, year, current/archived status, and relationship to this thesis are **unverified**. | None. | No claim is made about the course's current relevance or administrative requirements. In particular, it is not assumed to be the current thesis seminar. |

The Edge window also showed a separate tab titled “Space Technologies for Intelligent, Sustainable and Autonomous Systems (2026).” Its relationship, if any, to either requested URL is unverified and it was not used as a source.

### Course-material prompt-injection audit

The Moodle requests yielded login screens rather than instructional content. Consequently, there was no course document text, hidden text, comments, annotation, or linked file available to inspect. **No suspicious instruction was observed, but the course materials were not screened; this is not a clean-source determination.** No external page's behavioral instructions were followed. Any eventual course AI-use rule or authentic course requirement should be checked against the current authenticated course page before use.

## Thesis, repository, and Drive coverage

| Source | Coverage status | How it supports the book | Limits |
|---|---|---|---|
| Local thesis manuscript under `thesis/` | Read the source tree and the relevant chapters, methods, architecture, implementation, evaluation, discussion, education, and bibliography excerpts. | Research questions, design, implemented architecture, experimental scope, evaluation metrics, and limitations. | This is repository LaTeX evidence, not a verified read of the live Google Doc. |
| `src/kvarken_eo/` and `tests/` | Read implementation modules for STAC, transformation, scene model, concurrency, provenance, catalog, API, raster and sea-ice code; reviewed the CDSE transport and corresponding test. | Actual interfaces, data flow, retry and validation boundaries, query logic, mathematical implementation, and test scope. | Code and offline tests do not prove live provider behavior or production deployment. The textbook task made no code changes. |
| `docs/experiments/experiment_report.json` and `.md` | Read. | Frozen 256-scene benchmark values and workload context. | Fixture-derived synthetic metadata run; not 256 independently acquired satellite scenes, live CDSE, raster throughput, or cloud performance. |
| `docs/experiments/experiment_report_live_20260915.json` and `.md` | Repository contains the dated artifacts; their status is described in repository documentation and thesis source. | Explicit offline-fallback distinction. | The artifact filename does not establish live CDSE success; it is an offline fallback. |
| `docs/research/20261019/` | Read README, results, case configuration, manifests, source licenses, figures, and relevant record excerpts. Independently checked requested counts and derived ratios from the result record. | Real Sentinel observations, preprocessing, proxy rules, spatial split, LDA, held-out metrics, areas, images, checksums, and caveats. | Large raster windows and full original SAFE packages are not checked in. Recorded checksums identify retained derived windows, not complete original products. |
| `docs/CSC_DEMONSTRATION.md` and CSC run records | Read. | Five-record CSC metadata/provenance/catalog/regional-query/loopback-API replay. | Not raster retrieval, remote classification, distributed-scale processing, or a cloud-speed comparison. |
| Supplied thesis Google Doc URL | Not independently inspected in this task. | The repository manuscript is used as the accessible thesis evidence. | The live document may contain edits not present in the local source. No synchronization claim is made. |
| Supplied Google Drive folder | Not independently inspected in this task. | None. | Contents and the exact location/identity of the original book are not verified. No file was edited or uploaded. |
| Supplied GitHub repository URL | Local checkout source was used. | Public repository reference and cited source paths. | This task did not make a remote GitHub change or verify that a remote branch contains the derivative. |

### Implementation discrepancy requiring notice

The manuscript describes the CDSE adapter as supplying a bearer token. In the checked-in implementation, `src/kvarken_eo/cdse.py::BearerSTACTransport.set_authorization` builds `Bearer ` plus the supplied token, and `tests/test_cdse.py::test_bearer_transport_sends_access_token_in_authorization_header` checks that header. This is offline verification only, not proof of successful live CDSE authentication. This discrepancy is disclosed in Lessons 7 and 8. The book does not claim successful live CDSE authentication, and this document task did not change the repository code.

## Chapter-to-source coverage

| Book lesson | Repository thesis / implementation evidence | External scientific or technical support | Moodle |
|---|---|---|---|
| 1. How do we know? | `thesis/chapters/01_introduction.tex`; `03_methodology.tex`; `docs/THESIS_SUMMARY.md` | NASA Earthdata EO basics [3–4] | Not accessible |
| 2. Earth-to-satellite signal | `thesis/chapters/02_background.tex`, `04_implementation.tex`; `src/kvarken_eo/sea_ice.py` | NASA spectrum/active sensing [3–4]; Small [9]; Dierking [10] | Not accessible |
| 3. Missions and Kvarken | Thesis background and raster methods; `case_config.json`; `captured_scenes.json` | ESA/Copernicus Sentinel mission documentation [1–2]; UNESCO geology context [21] | Not accessible |
| 4. Pixels and maps | `src/kvarken_eo/spatial.py`, `raster.py`; `results.json` | IOGP EPSG dataset [6]; OGC GeoTIFF [22] | Not accessible |
| 5. Mathematics and evaluation | `src/kvarken_eo/sea_ice.py`; thesis evaluation and implementation | Drusch et al. [8]; Park et al. [11]; Dierking [10] | Not accessible |
| 6. Programming and computers | `pyproject.toml`; implementation modules and tests; `README.md` | Python documentation [18]; SQLite WAL [7] | Not accessible |
| 7. STAC and EO services | `src/kvarken_eo/stac.py`, `cdse.py`; thesis background; CSC evidence | STAC 1.1 [5]; CDSE [12]; Google Earth Engine [13]; Planetary Computer [14]; openEO [15]; CSC [16]; Pangeo [17] | Not accessible |
| 8. Pipeline and provenance | Architecture/implementation chapters; `stac.py`, `transform.py`, `models.py`, `concurrent.py`, `provenance.py`, `catalog.py`, `api.py` | STAC [5]; SQLite [7] | Not accessible |
| 9. Performance evidence | `docs/experiments/`; thesis methodology/evaluation | Source-specific platform documentation as relevant [12, 14, 16] | Not accessible |
| 10. Sea-ice case | Thesis implementation/evaluation/discussion; `docs/research/20261019/`; actual figure PNGs | Sentinel documentation [1–2]; WorldCover [19]; Small [9]; Dierking [10]; Park et al. [11] | Not accessible |
| 11. Reproduction and critique | `09_education_innovation.tex`; `appendix_repro.tex`; README; CSC records | CSC documentation [16]; Python [18] | Not accessible |

The complete source-to-chapter matrix and reference list also appear inside the textbook for NotebookLM ingestion.

## External source verification and attribution

The external sources in the book were selected from ESA/Copernicus mission documentation, NASA Earthdata educational documentation, the OGC STAC and GeoTIFF standards, IOGP/EPSG, SQLite, Python, UNESCO, platform documentation, and peer-reviewed papers. Public pages were fetched or checked by a specialist source-verification pass on 26 October 2026. Dynamic operational pages are identified as time-sensitive; values for the March 2021 case are not presented as current constellation status.

The research figures are actual thesis-derived PNGs in `docs/research/20261019/`; their captions distinguish source observation, upstream processor, host/distributor, and thesis classification. The image captions retain the attribution in the repository's `source_licenses.json`. Other diagrams in the book are newly written conceptual tables and verbal descriptions, not observed satellite scenes. Classroom numbers are explicitly marked illustrative.

## Final access and editing status

- The Markdown source was rendered locally by `docs/education/render_book.py` to `Kvarken_Thesis_Learn.docx` and `Kvarken_Thesis_Learn.pdf`; the PDF is 41 pages and embeds all six case-study figures.
- Read-back checks found all 11 lesson headings, the cited benchmark and sea-ice result values, six embedded images in each edition, 14 DOCX tables, and descriptive text accompanying the figures. The PDF was rendered to page images and visually inspected for the cover, lesson pages, equations, tables, case-study maps, and final references/roadmap.
- The DOCX was reopened and structurally checked with `python-docx`; lesson headings have page breaks and each embedded figure has alternative text. No Word/Office visual rendering was available in this environment.
- Original attached `Kvarken_theses_learn.docx`: **not found in the worktree or session files inspected; content not read**.
- Exact existing Google Doc for the educational book: **not safely resolved**. A Google Docs tab with a similar title was visible in Edge, but active-user interruption prevented inspection. The supplied Google Doc link in the task is for the thesis manuscript; it is not treated as the book's document.
- Google Drive folder: **not opened**. No upload, sharing change, or permission change was attempted.
- Moodle section 51091: **login required; course identity and content unverified**.
- Moodle course 5192: **login required; course identity and content unverified**.
- Thesis code, data, and experiment records: **not modified**.
- The Markdown, DOCX, and PDF are new local derivatives. They do not replace or synchronize any Google Drive or Moodle document.
