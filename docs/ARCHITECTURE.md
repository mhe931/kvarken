# Architecture

## Current vertical slice

```text
EODataSource
    |
    v
AsyncIngestor -- RetryPolicy --> typed payload validation --> EOScene
    |
    v
IngestionResult (source, scene, attempts)
```

`EODataSource` is an async protocol. `MockEODataSource` simulates provider responses without network access. `AsyncIngestor` owns retry decisions and never retries validation failures. The scene model is deliberately transport-neutral so spatial transforms can be added without coupling them to an HTTP client.

## Failure taxonomy

- `FetchTimeout`: transient source timeout; retry with capped exponential backoff.
- `RateLimitExceeded`: transient provider throttling; retry using the provider delay when supplied.
- `PayloadValidationError`: permanent malformed or incomplete source payload; fail immediately.

## Extension points

Future provider adapters should translate provider-specific responses into the `RawScenePayload` mapping and retain source identifiers and acquisition timestamps. Persistent storage and spatial processing should consume `EOScene`, not provider-specific objects.
