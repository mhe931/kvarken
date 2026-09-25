# Thesis final deliverables

Prepared on 2026-09-25 for:

**Design and Implementation of a Hybrid Earth Observation Data Infrastructure for Research and Education: A Case Study of Kvarken Space Center**

Author: Daniel Ebrahimzadeh Esfahani  
Programme: Master's Degree Programme in Computing Sciences  
Major: Artificial Intelligence and Data Engineering  
Supervisor: Professor Ali Nadir Arslan  
University: University of Vaasa, School of Technology and Innovations

## Authoritative working artifacts

- Final submission candidate DOCX in Google Drive: https://docs.google.com/document/d/13MbaQnKQHF_CCKkgG_GumUyHhb3A7EEd/edit
- Final scientific defense presentation: https://docs.google.com/presentation/d/1lWYzgYt7Gtt7xeWIbQuzhAZz87CkbP3xW4oZC5vSHQo/edit
- 20-minute thesis progress presentation: https://docs.google.com/presentation/d/1QTyciM7cg8vAszsHBpBuoQxTkVx4bKWPY6q5YFdzl4k/edit

The final candidate is approximately 39 rendered pages and 9,480 words. The repository keeps the reproducible LaTeX manuscript under `thesis/`; the Drive DOCX is the current supervisor-review copy.

## Scientific structure synchronized in this branch

The manuscript now contains:

1. Introduction
2. Background and Literature Review
3. Methodology
4. System Architecture
5. Implementation
6. Results
7. Analysis
8. Discussion
9. Conclusion and Future Work
10. References
11. AI-assisted work disclosure
12. Reproducibility and claim-boundary appendix

The scientific narrative is:

**research gap -> methodology -> design decisions -> controlled evidence -> RQ analysis -> discussion -> limitations -> conclusion**

## Verified evidence boundary

The thesis uses the repository experiment artifacts as the source of truth:

- 256 synthetic scenes
- concurrency = 8
- elapsed time = 1.159317 s
- throughput = 220.819653 items/s
- failures = 0
- retries = 0
- spatial query latency = 9.117 ms
- released baseline records 53 passing offline tests
- dated 20260915 experiment is explicitly `offline-fallback` / `offline-fixture`

These values must not be described as authenticated CDSE or production-scale performance.

## Submission boundary

This is a submission candidate, not an institutionally approved final submission. Remaining gates are supervisor review, any required official University template/logo adjustments, final accessibility/reference checks, Turnitin, and the University of Vaasa Osuva/PDF-A workflow.
