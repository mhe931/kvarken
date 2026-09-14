# Roadmap

## Foundation (complete)

- Typed source and scene contracts
- Offline mock provider
- Explicit transient failure retries
- Tests and continuity documentation

## Provider integration

- Implement one public EO catalog adapter.
- Add authentication through environment variables or managed identity only.
- Record request IDs, source URLs, and acquisition timestamps.

## Processing

- Add cloud-optimized raster metadata and spatial reference validation.
- Introduce deterministic tile/window transforms.
- Add small fixture-based integration tests.

## Evaluation and operations

- Measure throughput, retry behavior, and memory use under bounded concurrency.
- Add structured logging and metrics hooks.
- Document reproducibility and thesis experiment procedures.
