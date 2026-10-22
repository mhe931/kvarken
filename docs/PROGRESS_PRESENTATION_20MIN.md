# 20-minute thesis progress presentation

> Working local outline for the current thesis source. The linked Google Slides file has
> not been updated or verified in this revision. Do not use prior page counts as current.

Native Google Slides: https://docs.google.com/presentation/d/1QTyciM7cg8vAszsHBpBuoQxTkVx4bKWPY6q5YFdzl4k/edit

## Current 12-slide narrative

1. Thesis title, University context, and scope
2. Research purpose, gap, and questions
3. Comparative EO platform landscape: CDSE, Earth Engine, Planetary Computer, CREODIAS,
   openEO, Pangeo, and Open Data Cube
4. Hybrid architecture and what the prototype reuses or implements
5. Provider boundaries: offline CDSE tests versus Planetary Computer raster access
6. Student workflow: onboarding through independent reproduction, with evidence status
7. Sentinel-1/Sentinel-2 case selection, WorldCover role, and provenance
8. Validation design and optical-proxy label limits
9. Results and interpretation: 88.00% ordinary agreement, 23.53% ice precision, and
   95.99% always-water agreement on selected labelled cells
10. Education and research capabilities demonstrated versus future proposals
11. Threats to validity, reproducibility, and remaining tests
12. Current status, open supervisor/institutional gates, and next steps

## Evidence to keep visible

- The 256-scene benchmark is synthetic and uses the offline baseline.
- The 20260915 report is an offline fallback, not evidence of authenticated CDSE success.
- The CSC demonstration replayed five captured metadata records through provenance, catalog
  queries and a loopback API; raster classification ran locally.
- The optical-proxy metrics describe selected labelled cells, not all candidate pixels or
  field-validated ice extent.
- The in-house prototype reuses established standards and hosted services; it is not a
  replacement for global EO platforms.
- Student learning outcomes, cost savings, multi-user operation, remote CSC raster processing
  and live CDSE pixel access have not been demonstrated.

## Manuscript and export status

The previous source revision produced a 69-page CI PDF and an 82-page Word-rendered review
PDF. The platform-comparison, workflow and abbreviation changes in the current branch have
not yet been compiled or paginated. Those previous counts are historical and must not be
presented as current. The current branch has not passed Python/Ruff checks, official-template
DOCX export, PDF/A validation or accessibility review.

The abstract is 442 words and does not include the specific numeric study results. Current
page numbers and the contents/list pages remain subject to a new build.

## Submission sequence

Author review -> current-source build and correction -> supervisor review -> written
permission for Turnitin -> review of the similarity report -> final accessible and validated
file -> Osuva submission under the programme's instructions. This sequence is a plan; no
email, Turnitin submission, Osuva submission or supervisor approval is claimed.

The exact defence/seminar duration and individual submission deadline require confirmation
from the supervisor or programme.
