# Kvarken EO Pipeline

Production-minded research scaffold for hybrid Earth Observation (EO) data ingestion and processing in the Kvarken Space Center context. The repository favors small, typed, async-aware components that can be extended during weekly research checkpoints without losing continuity.

## Prerequisites

- Python 3.11 or newer
- Git

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Verify

```powershell
python -m pytest
python -m ruff check .
python -m ruff format --check .
```

The package includes a dependency-free STAC client built on the Python standard library. Its transport is injectable, so tests and research runs can remain offline. The initial demo still uses an in-memory EO source:

```powershell
python -m kvarken_eo --demo
```

## Repository map

- `src/kvarken_eo/` - ingestion contracts, STAC adapter, validation, provenance sink, and CLI demo
- `tests/` - unit tests, offline STAC fixtures, and provenance verification
- `docs/` - goals, architecture, current status, and roadmap
- `AGENTS.md` - continuity and contribution rules for people and coding agents

## Development conventions

Keep source code under `src/`, add a focused test for every behavior change, and update the relevant document in `docs/` when a milestone or architectural decision changes. Do not commit credentials, raw datasets, generated artifacts, or local environment files.

### Concurrent ingestion

`ConcurrentEOIngestor` transforms and persists STAC items with a bounded `max_workers` semaphore. The default is four workers; use a lower value when a provider has stricter rate limits:

```python
from pathlib import Path

from kvarken_eo import ConcurrentEOIngestor, FileProvenanceSink, STACClient

pipeline = ConcurrentEOIngestor(
    STACClient("https://earth-search.aws.element84.com/v1"),
    FileProvenanceSink(Path("data/staged")),
    max_workers=2,
)
results = await pipeline.search_and_ingest(collections=("sentinel-2-l2a",))
```

The provenance sink serializes JSONL appends with an async lock and performs filesystem work in a worker thread, keeping the event loop responsive.
