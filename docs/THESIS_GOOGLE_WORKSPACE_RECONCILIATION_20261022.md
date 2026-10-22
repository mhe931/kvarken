# Thesis reconciliation checkpoint — 22 October 2026

This checkpoint records observed Google Workspace actions, not thesis submission readiness.

## Verified edits

- Main native Google Doc: https://docs.google.com/document/d/1oq5FtrWh4Yb3yd2NBtUS0OgNO2jtuDUMqzVz0085lEE/edit
- Academic-review Google Doc: https://docs.google.com/document/d/1y1OaL6Yrqx1FFgVTwdU-L2P1SnSb5Moo3HK9i8ru7Kg/edit
- Replaced seven exact textual divergences in the main Doc against the academic-review copy (evaluation-layer count; offline fallback telemetry name and interpretation; science provenance language; incomplete temporal-gap sentence; two bibliographic details). Connector reports one occurrence replaced per change.
- Verified both native documents by second read: 586 paragraphs each and zero differences in extracted paragraph text. This verifies extracted-text parity between those two copies, **not parity with the latest LaTeX v16 manuscript**, images, tables, page layout, comments, or supervisor access.
- Updated 12-slide progress deck: https://docs.google.com/presentation/d/1QTyciM7cg8vAszsHBpBuoQxTkVx4bKWPY6q5YFdzl4k/edit
- Updated 14-slide defense deck: https://docs.google.com/presentation/d/1lWYzgYt7Gtt7xeWIbQuzhAZz87CkbP3xW4oZC5vSHQo/edit
- Read both decks back; verified all titles, text and slide counts. No slide-by-slide visual rendering audit was completed.

## Outstanding blockers

1. **Critical source parity:** Latest LaTeX `thesis/chapters/02_background.tex` has a comparative EO platform review and table, including Google Earth Engine, CREODIAS, openEO, Pangeo/Open Data Cube, plus other services. Neither native Google Doc contains that material yet. The local and repository source remains authoritative for this expansion. Synchronize source-complete document safely while retaining existing images/fields/styles, compare citations and references, and verify all sections.
2. **Current export:** The review log says v16 Word PDF has 94 pages; the exact PDF was not available through this session's connected sources. Full 94-page visual audit has not been completed here.
3. **Independent standards verification:** v16 XMP PDF/A-3a and document structure tags are declarations only. Run independent validator such as veraPDF plus a tagged-PDF reading-order/accessibility audit.
4. **Institutional requirements:** Independently verify current University of Vaasa instructions against the final artifact, especially citations, acronyms, abstract, typography, tables, PDF, Turnitin and Osuva sequencing.
5. **Presentation visual QA:** Export both newly revised Google Slides files and inspect every slide for overflow, cropping, factual consistency and citations. Draft progress/defense slides must not be represented as final before visual review.
6. **Supervisor and sharing:** Confirm Professor Arslan's intended Doc access; the Drive listing does not establish it. Request manuscript supervision/approval; neither supervisor nor academic review is replaced by code review.
7. **PR #30:** Open and mergeable at last connector check. Copilot review state COMMENTED, not APPROVED. Obtain appropriate review approval before merge. Do not merge merely because CI is green.

## Evidence discipline

- Keep 256-scene benchmark labeled synthetic and the 20260915 report labeled offline fallback.
- CSC demonstration covers five captured metadata scene records through provenance, SQLite catalog, regional query and loopback API; **not** remote raster processing.
- Sentinel raster classification was local. Optical proxy labels have a 17.90-hour mismatch; 88.00% ordinary agreement, 23.53% ice precision, and 95.99% always-water baseline agreement apply only to selected labeled cells. Candidate area is not validated sea-ice extent.
- The 104 passing tests and the reported five green CI checks in the preceding user status are historical checkpoints; this documentation-only commit does not constitute a rerun.

Status: review in progress, **not submission-ready**.
