import pytest

from kvarken_eo.ingestion import (
    AsyncIngestor,
    FetchTimeout,
    RateLimitExceeded,
    RetryPolicy,
)
from kvarken_eo.models import PayloadValidationError

VALID_PAYLOAD = {
    "scene_id": "scene-001",
    "platform": "SENTINEL-2",
    "acquired_at": "2026-09-14T12:00:00+00:00",
    "cloud_cover": 10,
    "footprint": [(21, 63), (21.1, 63), (21.1, 63.1)],
}


class SequenceSource:
    def __init__(self, *responses):
        self.responses = list(responses)
        self.calls = 0

    async def fetch(self, scene_id):
        self.calls += 1
        response = self.responses.pop(0)
        if isinstance(response, BaseException):
            raise response
        return response


@pytest.mark.asyncio
async def test_ingest_validates_and_returns_scene():
    source = SequenceSource(VALID_PAYLOAD)

    result = await AsyncIngestor(source).ingest("scene-001")

    assert result.scene.scene_id == "scene-001"
    assert result.attempts == 1


@pytest.mark.asyncio
async def test_timeout_is_retried_then_succeeds():
    source = SequenceSource(FetchTimeout(), VALID_PAYLOAD)
    ingestor = AsyncIngestor(source, RetryPolicy(base_delay=0, max_delay=0))

    result = await ingestor.ingest("scene-001")

    assert result.attempts == 2
    assert source.calls == 2


@pytest.mark.asyncio
async def test_rate_limit_uses_retry_after_and_exhaustion_is_explicit():
    source = SequenceSource(RateLimitExceeded(retry_after=0), RateLimitExceeded(retry_after=0))
    ingestor = AsyncIngestor(source, RetryPolicy(max_attempts=2, base_delay=0, max_delay=0))

    with pytest.raises(RateLimitExceeded):
        await ingestor.ingest("scene-001")

    assert source.calls == 2


@pytest.mark.asyncio
async def test_corrupted_payload_is_not_retried():
    source = SequenceSource({"scene_id": "broken"})

    with pytest.raises(PayloadValidationError):
        await AsyncIngestor(source).ingest("scene-001")

    assert source.calls == 1


@pytest.mark.asyncio
async def test_empty_scene_id_is_rejected_before_source_call():
    source = SequenceSource(VALID_PAYLOAD)

    with pytest.raises(ValueError, match="scene_id"):
        await AsyncIngestor(source).ingest(" ")

    assert source.calls == 0
