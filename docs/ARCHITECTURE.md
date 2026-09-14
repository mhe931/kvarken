# Architecture

## Current vertical slice

```text
STACClient -- RetryPolicy --> STACTransport --> public STAC API
    |                                  |
    v                                  v
validated STACItem                FileProvenanceSink
                                       |
                                       v
                              raw JSON + manifest.jsonl
```

`STACClient` queries the standard `/search` endpoint, follows `next` links, and retries only timeout and rate-limit failures. `STACTransport` is injectable; `UrllibSTACTransport` provides a dependency-free production implementation. `MockEODataSource` remains available for the original scene-ingestion slice.

`FileProvenanceSink` writes canonical raw JSON under a content-addressed SHA-256 filename and appends an audit record containing source identity, collection, URI, timestamp, retry attempts, and relative raw-payload path.

`transform_stac_to_scene` maps STAC geometry or bbox, `proj:epsg`, assets, platform, acquisition datetime, and optional `eo:cloud_cover` into `EOScene`. `ConcurrentEOIngestor` uses `asyncio.Semaphore` to cap transformation and persistence workers. `store_async` serializes each sink's manifest append with an `asyncio.Lock` and delegates blocking filesystem operations to a thread.

## Failure taxonomy

- `FetchTimeout`: transient source timeout; retry with capped exponential backoff.
- `RateLimitExceeded`: transient provider throttling; retry using the provider delay when supplied.
- `PayloadValidationError`: permanent malformed or incomplete source payload; fail immediately.

## Extension points

Future provider adapters should translate provider-specific responses into typed records and retain source identifiers and acquisition timestamps. Spatial processing should consume validated records, not provider-specific transport objects.
