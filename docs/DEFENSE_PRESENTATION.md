# Final thesis defense presentation

Native Google Slides: https://docs.google.com/presentation/d/1lWYzgYt7Gtt7xeWIbQuzhAZz87CkbP3xW4oZC5vSHQo/edit

## Current 14-slide narrative

1. Title and thesis scope
2. Research design and methodology
3. Research problem and gap
4. Research questions and evidence
5. Hybrid architecture
6. Provider boundary and validation
7. Bounded ingestion and provenance
8. Kvarken spatial catalog
9. Evaluation design
10. Frozen baseline results
11. Research contributions
12. Threats to validity
13. Future work
14. Conclusion and questions

## Defense claim

A small EO research infrastructure can be made auditable and reproducible when provider boundaries, bounded work, provenance, spatial persistence, and evidence artifacts are explicit.

The defense must also state the boundary:

> The thesis demonstrates a controlled research baseline, not a production-scale EO platform.

## Evidence discipline

- The 256-scene run is a controlled synthetic metadata benchmark.
- 220.819653 items/s is local metadata-path throughput, not CDSE throughput.
- 9.117 ms is a frozen local spatial-query value, not a general latency guarantee.
- The 20260915 artifact is `offline-fallback`, not authenticated CDSE.
- The raster slice is byte-range/downsampling/NDVI validation, not complete GeoTIFF processing.
- Educational access is implemented, but learning outcomes were not evaluated.
