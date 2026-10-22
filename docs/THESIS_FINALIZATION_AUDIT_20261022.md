# Thesis synchronization and independent review checkpoint — 22 October 2026

**Status: supervisor-review candidate; NOT submission-ready.** This is a record of actual checks and updates, not a claim of independent PDF/A conformance or academic approval.

## Evidence anchors

- Original native Google Doc: https://docs.google.com/document/d/1oq5FtrWh4Yb3yd2NBtUS0OgNO2jtuDUMqzVz0085lEE/edit
- Historical academic-review copy (retained without further alteration): https://docs.google.com/document/d/1y1OaL6Yrqx1FFgVTwdU-L2P1SnSb5Moo3HK9i8ru7Kg/edit
- Canonical source: `thesis/chapters/02_background.tex`, `thesis/chapters/09_education_innovation.tex` and `thesis/references.bib` on `main` after PR #30.
- Professor's historical topic and September first-meeting notes: https://drive.google.com/drive/folders/1huJvQ1obmJl4ao7lM6mbB84RMOhzU-qf
- Prior supervisor response matrix: `docs/THESIS_REVIEW_RESPONSE_20261022.md`.
- Official university requirements: https://www.uwasa.fi/en/students/writing-guidelines-and-plagiarism-detection/writing-guidelines and https://www.uwasa.fi/en/students/masters-thesis

## Verified Google Doc changes

1. Inserted `2.3 Comparative EO access and processing environments` based on canonical TeX source. Added source-aligned discussion of platform types, standards, providers, commercial alternatives, source ownership, the provider/local split, and CSC student suitability. Added an editable Google Docs table with **8 rows by 4 columns**, all **32 cells nonempty**; seven platform/ecosystem entries: CDSE, Google Earth Engine, Microsoft Planetary Computer, CREODIAS, openEO, Pangeo and Open Data Cube. Renumbered subsequent Chapter 2 sections to 2.4–2.8.
2. Inserted `9.2 Student workflow and implementation evidence`, nine-stage textual workflow/caption and an editable evidence table with **10 rows by 3 columns**, all **30 cells nonempty**. Renumbered following Chapter 9 sections to 9.3–9.5. The source TikZ diagram's **semantics** were represented in text; the source vector diagram has **not** been reproduced as a Google Docs graphical object.
3. Rebuilt the Google Docs references from all **36 entries** in the canonical `.bib`, keeping source DOIs or URLs and alphabetic first-author ordering. Applied specific corrections to citation text and author spelling. The rebuilt list is *source-aligned, not independently bibliographically certified*. Every DOI, retrieval-date and in-text disambiguation still needs final APA/University of Vaasa audit.
4. Removed **15 stale physical-page numbers** from the old manually entered Contents, because insertion changed pagination. This is a review-state safeguard, not a final contents solution. Regenerate and visually check all contents, list-of-figures, list-of-tables and page/section references for the approved final export.
5. Older pre-audit and academic-review copies remain unchanged. Consequently the current Google Doc deliberately no longer has complete text parity with the historical review copy. Full text, table, illustration and PDF-render equivalence against the final v16 TeX/Word export is **not yet established**.

## Presentation checks

- Progress deck: https://docs.google.com/presentation/d/1QTyciM7cg8vAszsHBpBuoQxTkVx4bKWPY6q5YFdzl4k/edit — 12 slides; body and title text revised against thesis facts in previous reconciliation.
- Defense deck: https://docs.google.com/presentation/d/1lWYzgYt7Gtt7xeWIbQuzhAZz87CkbP3xW4oZC5vSHQo/edit — 14 slides; body and title text revised in previous reconciliation.
- In this pass, structural reading found all **52** title/body text boxes exceeded the actual 16:9 Google Slides canvas (24 on progress, 28 on defense). Corrected their absolute transforms without deleting objects. Fresh API structural readback reports **zero page elements extending outside canvas in both decks**.
- **Not independently visually finished**: image pixels from Google Slides thumbnails / complete exported PDF slide pages could not be inspected in this runtime. Bounds fit does not rule out wrapping, clipped glyphs or unsuitable line breaks. Per-slide visual QA, accessible text reading order, and speaker notes should be verified before use.

## PDF and accessibility

- The supplied `Kvarken Thesis.docx` (a historical Google Docs-derived upload) produced **77 pages** when rendered locally with LibreOffice. It is **not** the separate **94-page v16** Word review PDF recorded in the previous GitHub response matrix.
- All 77 generated pages were checked structurally for nonblank extracted text and off-page text blocks, and all page thumbnails were assembled into contact sheets. No page was blank or had detected off-canvas text blocks. At high resolution, **page 12** shows a broken OAuth bearer-header formula; **page 32** has illegible grid-coordinate formula glyphs; **page 77** wraps the one-line PowerShell acquisition/reuse commands. This historical export must not be submitted.
- A local DOCX accessibility audit reports **seven HIGH-severity missing-image-alt-text findings** among seven inline images. This applies to the uploaded older copy, not necessarily to the separate v16 official Word export.
- The locally converted 77-page PDF is marked tagged but has no independently established PDF/A compliance. The **actual 94-page v16 PDF binary was not available in the provided upload, Google Drive folder or connected Drive PDF search**. Accordingly, a 94/94-page inspection and independent veraPDF/PDF/UA evaluation **have not been completed**. PDF/A XMP declarations, PDF tagging and accessibility are distinct checks; do not infer conformance from authoring/export settings.

## Professor Arslan / prior review crosswalk

- The Professor's early thesis topic describes a broader hybrid on-premise/cloud model, CSC student work, performance/cost/scalability/usability comparisons. The present manuscript appropriately restricts claims to implemented metadata paths, local science and a five-record CSC metadata replay; no completed multi-student study, commercial comparison experiment or cloud raster classification is demonstrated.
- The existing 12-row supervisor response matrix covers: CDSE vs Planetary Computer; research/teaching purpose; CSC boundaries; input/provenance; Figure 4.1; TOC/cross-references; bounded active concurrency; recovery not measured; classifier and candidate-area limits; clean-checkout reproduction; education/innovation; final editing.
- The historical folder contains a proposal and first-meeting documentation, **not an independently complete set of verbatim annotated supervisor comments or all ChatGPT/Gemini review reports**. Their full individual closure cannot be certified solely from the available files.
- The core scientific caveats remain: 256-scene benchmark synthetic; 20260915 experiment an offline fallback; Sentinel classifier agreement only on selected optical-proxy cells; 17.90-hour Sentinel-1/Sentinel-2 mismatch; 795.91 km² positive candidate area without optical reference; CSC replay metadata-only.

## Release gates

1. Compare the native Google Doc with the entire canonical v16 manuscript, including mathematical notation, source figures, caption order, references, and appendices; independently QA the bibliography and citations.
2. Obtain the **exact v16 94-page PDF** from the Word review export and visually check each page, tables, figures, fonts, TOC/LOF/LOT, reference links and Appendix B. Do not substitute the 77-page historical render.
3. Run **independent** PDF/A validation (for the actual target PDF) and structured/tagged-PDF accessibility validation; confirm reading order and alt text. Resolve all failures.
4. Export both current native decks, inspect **all 26 slides visually**, repair any overflow after transform correction, and check slide notes/citations.
5. Reconcile the response matrix with the complete original supervisor comments and both ChatGPT/Gemini reviews, mark each requirement as verified/corrected/not demonstrated with exact evidence.
6. Obtain Professor Arslan's review and approval before Turnitin. Submit the same approved file to Turnitin, then Osuva and Education Services as required by the university. No submission or professor authorization is asserted here.

**Disposition: audit documentation for human review. Do not represent this file or the Google Doc as a verified final thesis.**
