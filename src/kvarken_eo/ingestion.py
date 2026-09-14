"""Async ingestion contracts and bounded transient-failure handling."""

import asyncio
import random
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol

from .models import EOScene


class FetchTimeout(TimeoutError):
    """Raised when an EO source does not respond within its timeout."""


class RateLimitExceeded(Exception):
    """Raised when an EO source asks the client to slow down."""

    def __init__(self, retry_after: float | None = None) -> None:
        self.retry_after = retry_after
        super().__init__("EO source rate limit exceeded")


class EODataSource(Protocol):
    async def fetch(self, scene_id: str) -> Mapping[str, object]:
        """Fetch raw metadata for a scene."""


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    max_attempts: int = 3
    base_delay: float = 0.05
    max_delay: float = 1.0
    jitter_ratio: float = 0.0

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be at least one")
        if self.base_delay < 0 or self.max_delay < 0:
            raise ValueError("retry delays cannot be negative")
        if self.base_delay > self.max_delay:
            raise ValueError("base_delay cannot exceed max_delay")
        if not 0 <= self.jitter_ratio <= 1:
            raise ValueError("jitter_ratio must be between zero and one")

    def delay_for(self, attempt: int, random_value: float | None = None) -> float:
        delay = min(self.max_delay, self.base_delay * (2 ** max(0, attempt - 1)))
        if self.jitter_ratio:
            value = random.random() if random_value is None else random_value
            delay *= 1 - self.jitter_ratio + self.jitter_ratio * value
        return delay


@dataclass(frozen=True, slots=True)
class IngestionResult:
    scene: EOScene
    attempts: int


class AsyncIngestor:
    def __init__(self, source: EODataSource, policy: RetryPolicy | None = None) -> None:
        self._source = source
        self._policy = policy or RetryPolicy()

    async def ingest(self, scene_id: str) -> IngestionResult:
        if not scene_id.strip():
            raise ValueError("scene_id must be non-empty")

        for attempt in range(1, self._policy.max_attempts + 1):
            try:
                payload = await self._source.fetch(scene_id)
                return IngestionResult(EOScene.from_payload(payload), attempt)
            except (FetchTimeout, RateLimitExceeded) as error:
                if attempt == self._policy.max_attempts:
                    raise
                delay = error.retry_after if isinstance(error, RateLimitExceeded) else None
                await asyncio.sleep(
                    min(self._policy.max_delay, delay)
                    if delay is not None
                    else self._policy.delay_for(attempt)
                )

        raise AssertionError("retry loop must return or raise")
