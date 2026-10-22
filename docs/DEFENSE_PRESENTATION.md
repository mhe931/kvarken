# Final thesis defense presentation

> Working local outline based on the current thesis source. The linked Google Slides file
> has not been updated or verified in this revision; this is not a final defense deck.

Native Google Slides: https://docs.google.com/presentation/d/1lWYzgYt7Gtt7xeWIbQuzhAZz87CkbP3xW4oZC5vSHQo/edit

## Proposed 16-slide narrative

1. Title and thesis scope
2. Research objective, context and questions
3. Existing EO platforms and the specific research gap
4. Hybrid architecture and data boundaries
5. Implemented ingestion, validation and provenance
6. Spatial catalog, quality filters and educational API
7. Intended student workflow and stage-by-stage evidence status
8. Sentinel-1 and Sentinel-2 case selection, source attribution and timing
9. Optical-proxy labels and held-out evaluation design
10. Results: 88.00% ordinary agreement, 23.53% ice precision, and 95.99% always-water
    baseline agreement on selected labelled cells
11. Candidate area and missing optical reference: 1,219.28 km² candidate area and
    795.91 km² (65.28%) without optical labels
12. Interpretation: diagnostic agreement, not field accuracy or validated total extent
13. CSC demonstration: five metadata records, provenance, catalog and loopback API
14. Education and research contributions: implemented capabilities versus proposed benefits
15. Reproducibility, limitations, threats to validity and open institutional gates
16. Conclusion and questions

## Core defense claim

A small EO research infrastructure can make provider boundaries, validation, bounded active
work, provenance, spatial persistence and offline reproduction inspectable. The case study
also shows why a functioning pipeline is not, by itself, evidence of a reliable ice-extent
product.

## Evidence discipline

- ESA observations, upstream CATALYST RTC processing, Microsoft Planetary Computer hosting,
  and thesis-specific processing must remain distinct.
- The 2021 optical scene is not contemporaneous with the radar scene. Its labels are a
  selective proxy, not field ground truth.
- The 95.99% always-water baseline exceeds 88.00% ordinary agreement. Ice precision is
  23.53% on the selected labelled cells.
- The full candidate area is not validated ice extent; 795.91 km² of candidate area lacks
  optical labels (65.28% of the candidate area).
- The CSC work is a first-stage metadata/provenance/catalog replay. Raster processing ran
  locally; no student learning outcome was evaluated.
- The 256-scene benchmark is synthetic. The 20260915 artifact is offline fallback, not live
  CDSE evidence.

## Build and synchronization status

The previous source revision produced a 69-page CI PDF and an 82-page Word-rendered review
PDF. The current platform-comparison, CSC-workflow and abbreviation edits have not yet been
compiled. These page counts are historical. This outline is local documentation; no current
Google Slides synchronization, official-template export, PDF/A validation or accessibility
review is claimed.
