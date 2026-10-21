# Thesis review deliverables: 22 October 2026

Title unchanged: **Design and Implementation of a Hybrid Earth Observation Data Infrastructure
for Research and Education: A Case Study of Kvarken Space Center**.

- [Canonical manuscript source](../thesis/main.tex), ten chapters and two appendices.
- [Delivery report](THESIS_DELIVERY_REPORT_20261019.md), including historical evidence and blockers.
- [Review-response matrix](THESIS_REVIEW_RESPONSE_20261022.md), mapping the supplied review
  brief to revised sections, evidence and remaining limitations.
- [Actual-data maps, results, manifests and reproduction](research/20261019/README.md).
- [Official-template export/build procedure](../thesis/README.md).
- [Verified CSC metadata demonstration and reproduction boundaries](CSC_DEMONSTRATION.md).
- [Current-source XeLaTeX/Biber CI build (run 68)](https://github.com/mhe931/kvarken/actions/runs/39684624403).
- The 69-page CI review PDF was inspected for TOC/list numbering, cross-references, Figure 4.1,
  all five scientific figures and Appendix B. CI uses Carlito as its fallback font.
- A current-source DOCX was generated with the University June 2025 DOTX, APA CSL and Pandoc
  3.12.1. Headings, six figure captions, four table captions, image descriptions, metadata and
  the editable six-stage architecture diagram were inspected programmatically. The DOCX still
  requires Word field updates and visual repagination.
- The 19 October local DOCX/PDF exports and their 71/64-page counts are historical.
  The 22 October CI PDF is a source-build review copy; neither current export has current-source
  PDF/A or independent accessibility validation, and neither is an authorized submission
  candidate.
- Existing shared native Google Doc:
  https://docs.google.com/document/d/1oq5FtrWh4Yb3yd2NBtUS0OgNO2jtuDUMqzVz0085lEE/edit
  (not synchronized or verified on 22 October; the browser redirected to Google sign-in).

The pre-existing `Daniel_Ebrahimzadeh_Esfahani_Thesis_Final_Candidate.docx` and September
presentation materials remain historical. Do not email or present them as the revised
actual-data/CSC manuscript. No Google Slides update was performed.

The canonical chapter sequence is Introduction, Background, Methodology, System
Architecture, Implementation, **Evaluation** (Chapter 6), Analysis, Discussion,
In-House EO Infrastructure for Education and Research Innovation (Chapter 9), and
Conclusion and Future Work (Chapter 10).

This is not an approved final submission. Official-template DOCX export, author review,
supervisor authorization, verified synchronization, independent PDF/A/accessibility checks
and university submission procedures remain explicit gates. The historical CSC execution
is verified for metadata, provenance, catalog, regional queries and loopback API only;
remote raster classification was not performed.
