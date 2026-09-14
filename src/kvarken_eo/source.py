"""Offline source used for demos and deterministic tests."""

from collections.abc import Mapping

from .ingestion import EODataSource


class MockEODataSource(EODataSource):
    def __init__(self, payloads: Mapping[str, Mapping[str, object]]) -> None:
        self._payloads = payloads

    async def fetch(self, scene_id: str) -> Mapping[str, object]:
        return self._payloads[scene_id]
