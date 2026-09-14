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

`spatial.py` provides deterministic EPSG:4326 bbox and polygon intersection utilities. `KVARKEN_REGION_BBOX` is `(20.5, 62.8, 22.5, 63.8)`; closed-boundary intersection is intentional for study-area filtering. The benchmark harness injects latency and burst 429 responses into the STAC transport to verify retry recovery and zero record loss offline.

`SpatialCatalog` uses SQLite with a `scenes` table keyed by `scene_id`, indexed on `(platform, acquired_at)` and bbox columns. `query_scenes` first applies SQL range predicates to reduce candidates, then runs exact EPSG:4326 polygon checks. JSON columns preserve footprint and assets without external database dependencies. Writes use a process-local reentrant lock and explicit commits; `ConcurrentEOIngestor` delegates catalog writes to a worker thread.

Maintenance is explicit and locked: `prune_older_than` deletes records before a cutoff, while `vacuum` runs integrity checking, WAL checkpointing, and SQLite vacuuming. `FileProvenanceSink.find_orphaned_payloads` identifies raw files not referenced by active catalog scene IDs or beyond a filesystem retention cutoff. `prune_raw_payloads` is dry-run by default; deletion requires `dry_run=False`.

`python -m kvarken_eo verify-health` runs the complete offline fixture-to-provenance-to-catalog-to-query-to-maintenance path in a temporary directory.

`ConcurrentEOIngestor` exposes standard-library `IngestionMetrics` through `ingest_with_metrics()` and `last_metrics`. Metrics use monotonic elapsed time, canonical UTF-8 JSON byte counts, item attempt metadata for retries, and bounded-worker results. `.github/workflows/ci.yml` runs the same offline checks on Python 3.11 and 3.12 for pushes and pull requests to `main`.

`reports.py` converts metrics and catalog size/query latency into stable JSON plus a Markdown table. The `benchmark-report` CLI command synthesizes STAC items, runs the real concurrent ingestion/catalog path in a temporary directory, and exports artifacts to the requested output directory. `.pre-commit-config.yaml` keeps Ruff and basic whitespace checks consistent locally.

## Failure taxonomy

- `FetchTimeout`: transient source timeout; retry with capped exponential backoff.
- `RateLimitExceeded`: transient provider throttling; retry using the provider delay when supplied.
- `PayloadValidationError`: permanent malformed or incomplete source payload; fail immediately.

## Extension points

Future provider adapters should translate provider-specific responses into typed records and retain source identifiers and acquisition timestamps. Spatial processing should consume validated records, not provider-specific transport objects.
