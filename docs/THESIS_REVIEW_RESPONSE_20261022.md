# Supervisor review-response matrix

**Status: response matrix for the supplied 22 October 2026 brief; final pagination is
pending.** The most recent completed GitHub Actions XeLaTeX/Biber build is 82 pages, but it
predates the current local edits. The earlier v13 official-template DOCX was rendered in Word
to a 94-page review PDF. Its 429-word abstract is on page 2; the Contents (pages 3–6), figure
and table lists (pages 7–8), Figure 4.1 (page 36), and Figure/Table 9.1 (pages 73–74) show
populated page fields. Text extraction found no stale “Update field” or “Appendix 12” labels,
and a contact sheet plus selected-page renders was reviewed. A v14 official-template DOCX has
since been generated from the current local source and opened in Word, which reported 94 pages.
The current source abstract has 408 words and omits the specific performance comparisons. The
v14 Word PDF export is pending. Full-resolution page-by-page review, independent PDF/A
conformance and accessibility validation, and final Google Docs pagination remain incomplete.
This is not an authorized submission candidate.

The original email or annotated manuscript was not available, so this matrix maps the supplied
review brief, not unseen verbatim comments. Exact page references for the final Word and Google
Docs deliverables must be added after their final pagination is verified.

| # | Corrected section (page) | Change made | Supporting evidence | Remaining limitation |
|---|---|---|---|---|
| 1. CDSE versus Planetary Computer | Current CI: Chapter 2 (pp. 15–25; Table 2.1, pp. 16–21), Chapters 4–5 (pp. 31–45), Appendix B (pp. 78–82) | Separates CDSE OAuth2/STAC metadata interfaces and offline fake-transport tests from live provider evidence. Explains use of Planetary Computer-hosted CATALYST Sentinel-1 RTC COG assets, their spatial-window access and upstream RTC role. The current source adds the requested comparison with other EO platforms and ecosystems without claiming that the local system replaces them. | `tests/test_cdse.py`; `docs/research/20261019/`; `thesis/chapters/02_background.tex`; `thesis/chapters/04_implementation.tex`; `thesis/chapters/appendix_repro.tex` | No successful live CDSE metadata request or pixel download is confirmed. No additional live request was made. Final Word/Google Docs page references remain pending. |
| 2. In-house educational purpose | Current CI: Abstract (p. 2), Chapter 1 (pp. 11–14), Chapter 9 (pp. 65–69), Chapter 10 (pp. 70–73) | Makes University of Vaasa and Kvarken Space Center research and teaching the explicit purpose. Describes implemented offline metadata exercises, validation, provenance, catalog/API use, local real-data processing and the first-stage CSC metadata workflow. The current source adds a nine-stage workflow diagram and an evidence table that labels demonstrated, offline/local-tested, proposed and not-tested steps. | `thesis/chapters/00_abstract.tex`; `thesis/chapters/01_introduction.tex`; `thesis/chapters/09_education_innovation.tex`; `thesis/chapters/06_conclusion.tex`; implementation and test suite | No educational evaluation was performed; learning outcomes, student satisfaction and comparative benefits are not claimed. Final Word/Google Docs page references remain pending. |
| 3. CSC implementation boundaries | Current CI: Chapter 5 (pp. 44–45), Chapter 6 (pp. 56–57); Appendix B (pp. 80–82) | Describes project 2021696 as a verified first-stage research/educational prototype. Limits remote work to five authentic captured metadata records through provenance, SQLite catalog, regional queries and loopback API. States that raster classification ran locally. | `docs/research/20261019/csc_execution_evidence.json`; `docs/research/20261019/README.md`; `thesis/chapters/04_implementation.tex`; `thesis/chapters/appendix_repro.tex` | The CSC run does not evidence remote classification, large-scale raster processing, distributed execution, GPU acceleration or classifier-accuracy improvement. |
| 4. Input selection and provenance | Current CI: Chapter 5 (pp. 41–45), Chapter 6 (pp. 49–57; maps, pp. 51–55); Appendix B (pp. 78–80) | Documents Sentinel-1 on 30 March 2021, Sentinel-2 on 31 March 2021, the 17.90-hour mismatch, the single-case limitation and WorldCover 2021 v200 as an annual retrospective land mask. Separates ESA observations, CATALYST RTC preprocessing, Planetary Computer hosting/distribution and thesis processing; records identifiers and processing parameters. | `docs/research/20261019/case_config.json`; acquisition and quality-mask manifests under `docs/research/20261019/`; `thesis/chapters/appendix_repro.tex` | WorldCover is not a contemporaneous ice observation. Large raster windows are absent from Git and must be reacquired or supplied from a verified cache for a clean-checkout rerun. |
| 5. Figure 4.1 | Current CI: Chapter 4 (pp. 31–35; Figure 4.1, p. 33) | Replaces the text workflow with a source-controlled TikZ vector diagram for provider → transport/validation → EOScene → provenance/catalog → queries/API/reports → scientific application. Updates its caption and explanatory text. The DOCX exporter substitutes an editable six-stage flow diagram because Pandoc omits TikZ graphics. | `thesis/chapters/03_architecture.tex`; TikZ setup in `thesis/main.tex`; `thesis/export_documents.py`; regression assertion in `tests/test_manuscript.py`; v13 Word PDF (Figure 4.1, p. 36) | The LaTeX placement is verified, and the v13 Word diagram and caption were reviewed in the selected-page render. PDF tagging, alternative-text exposure and accessibility remain unverified. |
| 6. Contents, styles and cross-references | Current CI: TOC (pp. 3–5), lists of figures/tables (pp. 6–7), Figure 4.1 (p. 33), Appendix B (pp. 78–82) | Sets the LaTeX TOC depth to chapters and sections. Retains semantic chapter/section headings, a TikZ vector figure and styled command blocks. Configures Word TOC fields for levels 1–2 and updates contents, figure/table lists and page-reference fields in Word. | `thesis/main.tex`; `thesis/chapters/03_architecture.tex`; `thesis/chapters/appendix_repro.tex`; `thesis/export_documents.py`; `tests/test_manuscript.py`; current-source CI PDF and v13 Word PDF | The CI PDF has no unresolved `??` markers. The v13 Word PDF has numeric list/page references and no stale “Update field” or “Appendix 12” labels. Full visual review, final Google Docs pagination, and independent PDF/A/accessibility validation remain pending. |
| 7. Bounded concurrency | Current CI: Chapter 3 (pp. 27–30), Chapter 4 (pp. 31–35), Chapter 5 (pp. 36–37), Chapter 10 (pp. 70–73) | Uses “bounded active concurrency” for the semaphore guarantee and explicitly states that batch `gather` still schedules one coroutine per supplied item. Streaming scheduling is future work. | `src/kvarken_eo/concurrent.py`; `tests/test_concurrent.py`; `docs/ARCHITECTURE.md`; `AGENTS.md`; `thesis/chapters/03_methodology.tex`; `thesis/chapters/04_implementation.tex` | No constant scheduling-memory guarantee is made for unbounded input; streaming scheduling was not implemented. |
| 8. Recovery metric | Current CI: Chapter 6 (p. 48); Appendix B (pp. 80–81) | Interprets the frozen benchmark’s legacy recovery ratio of 1.000000 as a reporting convention, labels empirical recovery “not measured”/N/A because there were zero failures and retries, and identifies fault-injection tests as recovery evidence. | Frozen files `docs/experiments/experiment_report.json` and `docs/experiments/experiment_report.md` (unchanged); `tests/test_benchmarks.py`; `tests/test_cdse.py`; `tests/test_ingestion.py`; `thesis/chapters/05_evaluation.tex` | The frozen value remains in the immutable report for historical reproducibility and must not be interpreted as observed recovery. |
| 9. Scientific classifier claims | Earlier CI: Abstract (p. 2), Chapter 6 (pp. 49–57; figures, pp. 51–55), Chapter 8 (pp. 62–64), Chapter 10 (pp. 70–72) | Keeps selective optical-proxy validation distinct from full candidate-area inference. Reports 23.53% ice precision, 88.00% ordinary agreement, 95.99% always-water baseline agreement, 1,219.28 km² candidate area and 795.91 km² without optical reference in the results chapters. The current source abstract has 408 words and omits specific performance comparisons. | `docs/research/20261019/`; `thesis/chapters/00_abstract.tex`; `thesis/chapters/05_evaluation.tex`; five figure captions; `thesis/chapters/06_conclusion.tex`; `tests/test_manuscript.py`; August 2026 University writing guidelines | Results are from one case and a temporally mismatched optical proxy; they do not establish field accuracy, generalization or operational performance. The revised DOCX has not been rendered to PDF. |
| 10. Clean-checkout reproduction | Earlier CI: Appendix B (pp. 78–82; commands in B.4, pp. 80–82) | Rewrites reproduction instructions with separate commands for clone/environment, dependencies, tests, fresh acquisition, reuse and report generation. Corrects `--output-dir`, states expected success indicators and local software versions, and identifies untracked raster inputs. Fresh-acquisition and reuse examples now use short PowerShell path variables so flags remain on one logical command line. | `thesis/chapters/appendix_repro.tex`; verified output from `python -m kvarken_eo.case_study --help` and `python -m kvarken_eo --help`; v14 DOCX command paragraphs | A clean-checkout raster rerun was not performed; it requires network access or a retained verified input cache. Final PDF line wrapping has not been checked. |
| 11. Education and research innovation | Current CI: Chapter 9 (pp. 65–69), objective and contribution (pp. 12–13), conclusion (pp. 70–73) | Adds a concise chapter on inspectable processing, reproducible exercises, provider-neutral access, provenance, offline work, migration from local execution to CSC, extensibility, resource requirements and maintenance. Separates demonstrated capabilities from proposed benefits. | `thesis/chapters/09_education_innovation.tex`; corresponding objective and conclusion sections | Benefits are design rationale, not evaluated educational or economic outcomes. |
| 12. Final editing | Earlier CI: Abstract (p. 2), Chapters 1–10 (pp. 11–73), References (pp. 73–75), appendices (pp. 76–82) | Aligns objectives and claims, updates source attribution and AI disclosure, corrects identified scientific caveats and units, and reduces repeated limitations where feasible. The current source also expands the first-use definitions and alphabetical list of abbreviations. The v14 DOCX was generated and opened in Word; Word reported 94 pages. | Canonical sources under `thesis/chapters/`; `thesis/references.bib`; source regression tests; Daniel Academic Voice guidance | The v14 Word PDF export remains pending. Final pagination, full page-level visual review, Google Docs synchronization, independent proofreading, PDF/A and accessibility validation remain open. |

## Verification of the earlier source revision (not the current branch)

- Full Python suite: 93 tests passed.
- `ruff check .` and `ruff format --check .`: passed.
- Offline `verify-health`: passed.
- Current-source XeLaTeX/Biber build: passed in GitHub Actions; a 69-page PDF was downloaded
  and inspected for TOC/list page numbers, cross-reference markers, Figure 4.1, all five
  scientific figures and Appendix B.
- Historical Word export was generated with the official DOTX template and Pandoc 3.12.1.
  Word updated the TOC, figure/table lists and fields, and rendered an 82-page review PDF.
  Contents pages, Figure 4.1, all five scientific figures, tables and Appendix B were visually
  inspected; no stale “Update field” placeholders or unresolved cross-reference markers remain.
- The v13 official-template DOCX was rendered in Word to a 94-page review PDF. Text extraction
  and selected-page visual review confirmed the one-page 429-word abstract on page 2, populated
  Contents and list fields, Figure 4.1 on page 36, and Figure 9.1/Table 9.1 on pages 73–74.
  Table 9.1 has one header row in the DOCX; Word repeats that header on the continuation page.
  No “Update field” or “Appendix 12” text remains. The full-resolution page-by-page review and
  independent PDF/A/accessibility validation are incomplete.
- The current local follow-up has a 408-word source abstract and PowerShell reproduction examples
  with each invocation on one logical line. The 408-word abstract test passes. A v14
  official-template DOCX was generated, opened in Word, and saved; Word reported 94 pages. Its
  PDF export and final page-level visual review remain pending.
- Current local checks for this follow-up: 104 Python tests passed; Ruff lint and format checks,
  `git diff --check`, `verify-health`, and the offline demo passed. Pull-request CI has not yet
  run for these local edits.
- Independent current-source PDF/A/accessibility validation remains incomplete.
- Edge Personal opened the existing shared Google Doc and showed a saved-to-Drive status and a
  recent author edit attribution. After refresh, the content area rendered blank. No text or
  graphics were synchronized or verified, and the supervisor's access was not confirmed.
  The document identity was not changed.
- The source merged in PR #29 passed CI on Python 3.11 and 3.12 (83 passed and 3 skipped in
  each base test job), Ruff lint/format, health checks, optional science/document jobs, and
  XeLaTeX/Biber compilation. Its CI PDF reports 82 pages; that run predates the current local
  edits and is not CI evidence for this worktree. Official-template final rendering and current
  PDF/A/accessibility validation remain incomplete.
