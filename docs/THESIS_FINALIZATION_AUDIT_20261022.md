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


## Follow-up: current Google Docs PDF and full slide render inspection (22 October)

- Added 11 new abbreviation definitions to the original Google Doc (AWS, CSC, DEA, ESA, NASA, OData, ODC, REST, S3, SAS, SQL), verified 35 entries in the alphabetic abbreviation list. The source document itself is editable and no source manuscript numerical conclusions were changed.
- Exported the **current Google Doc** to an **88-page PDF** from Google Drive, not the older DOCX 77-page render or the unavailable official-template Word v16 **94-page** PDF. Structurally scanned all 88 pages: no blank pages and no detected off-canvas text blocks. Generated eight contact sheets and visually inspected pages 1-88 in order, plus enlarged platform and Chapter 9 evidence-table pages.
- Critical current Google Docs layout gap: the four-column source-platform comparison continues across several portrait pages (roughly PDF pp. 11-15) and is very dense, with the table header not repeated on continuation pages. The Chapter 9 evidence table continues across pp. 71-72. Mathematical expressions, page breaks, running references and the graphically simplified Figure 9.1 remain subject to final expert editorial review. The Contents is deliberately without stale page references rather than a validated auto-generated index.
- Current Google Docs PDF reports tagged PDF, PDF version 1.4, no visible PDF/A identifier, and **zero raw /Alt entries** for figures in the PDF object streams (low-level indicator only; not a substitute for full accessibility audit). This PDF is **not** independently PDF/A validated and must not be submitted as a conformant file.
- Obtained PDF exports of both revised native decks; **visually inspected all 12 progress slides and all 14 defense slides** as contact sheets. Layout is legible and none of the rendered titles or bodies visibly clips. Both decks underwent a structural check with zero page elements outside the actual 16:9 canvas after 52 shape transform repairs. Updated inaccurate progress slide 8 and slide 12 (PR #30 was merged); re-exported and inspected slide 12 at full resolution. This does not certify presentation academic approval.
- No independent veraPDF validator exists in this runtime, and neither the **exact official-template Word v16 94-page PDF** nor the full original supervisor annotations were accessible. Formal conformance and those reviews **remain blockers**.



## Third pass: official-guideline pagination, improved native comparison and PDF technical check (22 October 2026)

- Kept a native Google Docs backup before structural edits: [pre-layout backup](https://docs.google.com/document/d/1JBxxd0tlY9mzj_3aTamMIJruXu_sIHGJhDFmBxAVo7U/edit).
- Replaced the unreadable 8×4 EO platform matrix with a **22×2 native table**. This retains the full text of each of the original 7 platforms' three comparison dimensions, but separates dimensions into their own rows and uses approximately 155 pt / 270 pt column widths. Verified **44 nonempty cells**. This is semantically complete but not identical table structure to the canonical LaTeX.
- Corrected **five malformed formula/flow renderings** by comparing the Google Docs text with the canonical `03_architecture.tex` / `04_implementation.tex`; corrected **six bibliography disambiguation suffixes**. Created **36 active bibliography hyperlinks** in the editable Doc; new PDF contains **37 hyperlink annotations total**.
- Inspected University of Vaasa official [writing guidelines](https://www.uwasa.fi/en/students/writing-guidelines-and-plagiarism-detection/writing-guidelines). Applied native `pageBreakBefore` to 15 chapter, front-matter, reference and appendix headings. The Google Docs export became **94 pages**. Rebuilt the 15-item Contents with physically verified page positions: Acknowledgements 4; Abbreviations 5; Chapters 1–10 at 7,12,25,30,37,50,67,71,75,81; References 85; Appendices A/B 88/90. Re-exported and confirmed the page count and entry numbers.
- Generated **six contact sheets covering all 94 pages** and visually surveyed them. Structural text extraction found **zero blank pages** and **zero out-of-page text blocks**. The 2-column comparison renders legibly around pp. 13–17; actual raster figures remain present (7 image occurrences). Section headings and body are mainly Calibri bold 16/14 pt and Calibri 12 pt respectively.
- **PDF/A fails as current export**: the PDF catalogue has **no XMP Metadata entry and no OutputIntents**, which precludes treating the working Google Docs PDF as a conformant PDF/A delivery. It has `StructTreeRoot`, `MarkInfo/Marked true`, and `Lang(en)`, but **no detectable /Alt entries** for seven embedded images, so PDF/UA/accessibility compliance is not established. A standalone veraPDF release is unavailable in the runtime (official host could not resolve); **no independent standards-validator certificate** is claimed.
- **Further university-format problems remain**: page numbers appear at the **bottom center in Calibri 10 pt**, whereas Vaasa guidance requests **top center about 1.5 cm from the top at Calibri 11 pt**; formal lists of figures/tables are not yet present despite more than three visuals; static Contents should be regenerated after any further layout change; bibliography entries with ordinary URLs need their source-recorded retrieval dates and final Vaasa-APA style audit; the text-based Figure 9.1 is not a graphical parity reproduction; Google Docs embedded image alt-text is still absent. Some equations may still need author review for semantic equivalence.
- The **94-page Google Docs export is not proved equivalent to the separately reported 94-page Word v16 PDF**; identical page counts cannot establish parity. The latter file and a complete set of original supervisor annotated comments were not available. Professor Arslan's academic approval and Turnitin/Osuva steps are untouched.
- **Disposition: 94-page editable supervisor review candidate, NOT an approved PDF/A/accessible submission artifact.** Leave audit PR as draft and do not merge without review.
