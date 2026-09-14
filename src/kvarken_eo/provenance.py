"""Filesystem persistence for raw EO payloads and audit metadata."""

import asyncio
import hashlib
import json
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ProvenanceRecord:
    source_id: str
    collection: str
    source_uri: str
    payload_sha256: str
    ingested_at: str
    attempts: int
    raw_payload_path: str


class FileProvenanceSink:
    """Store canonical raw JSON and append one audit record per ingestion."""

    def __init__(self, root: Path) -> None:
        self._root = root
        self._raw_dir = root / "raw"
        self._manifest = root / "manifest.jsonl"
        self._lock = asyncio.Lock()

    async def store_async(self, **kwargs: object) -> ProvenanceRecord:
        """Persist without blocking the event loop and serialize manifest appends."""
        async with self._lock:
            return await asyncio.to_thread(self.store, **kwargs)

    def store(
        self,
        *,
        source_id: str,
        collection: str,
        source_uri: str,
        payload: Mapping[str, object],
        attempts: int = 1,
        ingested_at: datetime | None = None,
    ) -> ProvenanceRecord:
        if not source_id or not collection or not source_uri:
            raise ValueError("source_id, collection, and source_uri are required")
        if attempts < 1:
            raise ValueError("attempts must be positive")
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        self._raw_dir.mkdir(parents=True, exist_ok=True)
        raw_path = self._raw_dir / f"{digest}.json"
        raw_path.write_text(canonical + "\n", encoding="utf-8")
        timestamp = (ingested_at or datetime.now(UTC)).astimezone(UTC).isoformat()
        record = ProvenanceRecord(
            source_id,
            collection,
            source_uri,
            digest,
            timestamp,
            attempts,
            str(raw_path.relative_to(self._root)),
        )
        with self._manifest.open("a", encoding="utf-8") as manifest:
            manifest.write(json.dumps(asdict(record), sort_keys=True) + "\n")
        return record
