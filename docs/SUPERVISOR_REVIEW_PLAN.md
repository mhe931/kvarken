# Thesis status and draft work plan

**Author:** Däniel Ebrahimzadeh Esfahani  
**Supervisor:** Professor Ali Nadir Arslan  
**Date:** 5 October 2026  
**Status:** Draft for supervisor review

## Purpose and current position

I have prepared this plan to explain where the thesis stands and what I think remains before
submission. My aim is to complete the work by the end of December 2026, subject to your feedback
and the University's confirmed deadlines. I understand that you need to review the draft in
advance. The manuscript is therefore still a working draft.

The thesis concerns the design and implementation of a hybrid Earth Observation data
infrastructure for research and education, using Kvarken Space Center as the case study.
The repository contains a narrower implemented baseline: typed scene validation, bounded
asynchronous ingestion, provenance records, a SQLite spatial catalog, metadata quality
filters, a small raster-processing slice, and a read-only educational API. The wider hybrid
architecture remains the design context; its full deployment has not been demonstrated.

## Evidence available and its limits

The frozen experiment report contains 256 synthetic scenes at concurrency eight. It measures
the implemented metadata path, including validation, persistence, and spatial queries. The
reported cloud cover and asset completeness come from the fixture and do not describe the
actual distribution of Sentinel-2 acquisitions over Kvarken.

The dated 15 September report also ran in offline-fallback mode. It used one fixture scene
and a synthetic B04/B08 window. It provides a check of the numerical processing and reporting
path, but it does not demonstrate an authenticated CDSE run, full GeoTIFF decoding, or
production performance. I will keep these limits clear in the evaluation and discussion.

The checked-in tests cover validation, retry handling, provenance, bounded workers, catalog
queries, OAuth behavior with injected transports, and raster calculations. Software checks
support implementation integrity; they do not replace the additional research evidence that
may be needed for the final thesis.

## Questions for written feedback

I would appreciate your feedback on whether the current research scope is suitable and which
additional evidence you consider necessary. In particular, should I complete an authenticated
CDSE experiment and an analysis of representative raster windows before submission? I would
also appreciate guidance on how much educational and industrial validation is needed within
the remaining time.

I would prefer to continue the thesis communication by email so I can keep track of your
comments and refer to them while revising. I will send the status and plan as an attachment.
The draft email has not been treated as sent, and no approval has been assumed.

## Proposed remaining work

In October, I plan to revise the scope, research questions, and methods after your feedback
and agree the minimum additional evaluation. In November, I plan to carry out that evaluation,
record new results as dated artifacts, and send a revised manuscript for review.

In early December, I plan to address the remaining comments and check the references,
University template, and submission requirements. Final submission will follow your review
and the confirmed University process. This is a proposed schedule; the review time and
administrative deadlines still need to be confirmed.

## Document workflow

The working thesis and status documents in Google Drive are maintained as native Google Docs.
A Word file may be exported for an email attachment because the supervisor requested that
format. The repository's existing LaTeX sources remain available for reproducibility.
Empirical values must remain traceable to the frozen or dated experiment artifacts, and new
experiments must not overwrite the frozen baseline.
