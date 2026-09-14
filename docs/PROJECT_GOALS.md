# Project goals

## Research goal

Develop a reproducible, hybrid EO pipeline that can ingest satellite imagery and telemetry from heterogeneous sources, validate provider responses, and feed deterministic spatial analytics suitable for thesis evaluation.

## Engineering goals

1. Make provider boundaries explicit and replaceable.
2. Make transient failure handling observable, bounded, and testable.
3. Preserve provenance from source response through transformed output.
4. Support incremental weekly research checkpoints without undocumented conventions.
5. Keep the initial system runnable offline and free of credentials.

## Non-goals for the initial milestone

- Direct access to a commercial or public EO provider.
- Production orchestration or cloud deployment.
- Large fixture datasets checked into Git.
