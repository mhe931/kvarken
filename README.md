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

The initial vertical slice uses an in-memory EO source, so it does not require network credentials or external services:

```powershell
python -m kvarken_eo --demo
```

## Repository map

- `src/kvarken_eo/` - ingestion contracts, validation, retry policy, and CLI demo
- `tests/` - unit tests for successful and failure paths
- `docs/` - goals, architecture, current status, and roadmap
- `AGENTS.md` - continuity and contribution rules for people and coding agents

## Development conventions

Keep source code under `src/`, add a focused test for every behavior change, and update the relevant document in `docs/` when a milestone or architectural decision changes. Do not commit credentials, raw datasets, generated artifacts, or local environment files.

