# Agent continuity guide

## Purpose

`kvarken-eo-pipeline` is a thesis repository for hybrid Earth Observation data ingestion, validation, and spatial processing in the Kvarken Space Center context. The code should remain useful for reproducible research and operationally realistic experiments.

## Canonical commands

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest
python -m ruff check .
python -m ruff format --check .
python -m kvarken_eo --demo
```

## Architecture rules

- Keep application code under `src/kvarken_eo/` and tests under `tests/`.
- Model external data at the boundary with typed dataclasses; validate before transforms.
- Keep I/O async and injectable. Production adapters must implement the same protocol as test fakes.
- Keep retries explicit and bounded. Never retry malformed payloads; retry only transient timeout and rate-limit failures.
- Keep geospatial transforms deterministic and separate from transport concerns.
- Prefer standard library types and small modules over framework abstractions.
- Update `docs/PROJECT_STATUS.md` at each weekly checkpoint and record durable decisions in `docs/ARCHITECTURE.md`.

## Async and rate-limit safety

- Use bounded concurrency; do not create unbounded tasks from provider responses.
- Apply exponential backoff with a cap and honor a provider's retry delay when available.
- Set explicit network timeouts and propagate terminal errors with context.
- Do not mutate shared state from concurrent tasks without an explicit ownership boundary.
- Treat HTTP 429 and timeouts as transient; treat corrupted payloads and schema failures as permanent input errors.

## Milestone checklist

- [x] Repository identity and Python packaging established
- [x] Typed mock ingestion vertical slice implemented
- [x] Timeout, rate-limit, and corrupted-payload tests added
- [x] Developer and agent commands documented
- [ ] Add a real provider adapter behind `EODataSource`
- [ ] Add persistent raw/staged storage with provenance metadata
- [ ] Add spatial index and representative Sentinel-1/Sentinel-2 fixtures
- [ ] Benchmark bounded concurrent ingestion and document findings

## Change checklist

Before handing off work:

1. Add or update tests for changed behavior.
2. Run `python -m pytest`, `python -m ruff check .`, and `python -m ruff format --check .`.
3. Update status and roadmap documents when scope or milestones change.
4. Confirm no secrets, raw data, caches, or generated artifacts are staged.
