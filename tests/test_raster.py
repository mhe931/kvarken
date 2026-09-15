import pytest

from kvarken_eo.raster import RasterAssetFetcher, calculate_ndvi


class RangeTransport:
    def __init__(self):
        self.calls = []

    async def fetch_range(self, url, start, end, request_timeout):
        self.calls.append((url, start, end, request_timeout))
        return b"COG-window"


@pytest.mark.asyncio
async def test_fetcher_requests_inclusive_byte_range():
    transport = RangeTransport()
    fetcher = RasterAssetFetcher(transport)

    payload = await fetcher.fetch_band_range(
        {"B04": "https://assets.invalid/red.tif"}, "B04", 128, 255
    )

    assert payload == b"COG-window"
    assert transport.calls == [("https://assets.invalid/red.tif", 128, 255, 20.0)]


@pytest.mark.asyncio
async def test_fetcher_rejects_missing_band():
    with pytest.raises(KeyError, match="B08"):
        await RasterAssetFetcher(RangeTransport()).fetch_band_range({}, "B08", 0, 10)


def test_calculate_ndvi_handles_values_and_zero_denominator():
    assert calculate_ndvi((0.2, 0.0), (0.6, 0.0)) == pytest.approx((0.5, 0.0))


def test_calculate_ndvi_requires_matching_shapes():
    with pytest.raises(ValueError, match="equal lengths"):
        calculate_ndvi((1.0,), (1.0, 2.0))
