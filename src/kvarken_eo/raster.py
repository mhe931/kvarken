"""Small dependency-free raster asset and NDVI helpers."""

import asyncio
from collections.abc import Sequence
from typing import Protocol
from urllib.request import Request, urlopen


class AssetRangeTransport(Protocol):
    async def fetch_range(self, url: str, start: int, end: int, request_timeout: float) -> bytes:
        """Fetch an inclusive byte range from an asset."""


class UrllibAssetRangeTransport:
    async def fetch_range(self, url: str, start: int, end: int, request_timeout: float) -> bytes:
        return await asyncio.to_thread(self._fetch_range, url, start, end, request_timeout)

    @staticmethod
    def _fetch_range(url: str, start: int, end: int, timeout: float) -> bytes:
        request = Request(url, headers={"Range": f"bytes={start}-{end}"})
        with urlopen(request, timeout=timeout) as response:
            return response.read()


class RasterAssetFetcher:
    def __init__(
        self,
        transport: AssetRangeTransport | None = None,
        *,
        timeout: float = 20.0,
    ) -> None:
        if timeout <= 0:
            raise ValueError("timeout must be positive")
        self._transport = transport or UrllibAssetRangeTransport()
        self._timeout = timeout

    async def fetch_band_range(
        self,
        assets: dict[str, str],
        band: str,
        start: int,
        end: int,
    ) -> bytes:
        if band not in assets:
            raise KeyError(f"required band is missing: {band}")
        if start < 0 or end < start:
            raise ValueError("range must be non-negative and ordered")
        return await self._transport.fetch_range(assets[band], start, end, self._timeout)


def calculate_ndvi(red: Sequence[float], nir: Sequence[float]) -> tuple[float, ...]:
    """Calculate NDVI values, preserving zero-denominator pixels as 0.0."""

    if len(red) != len(nir):
        raise ValueError("red and nir bands must have equal lengths")
    values = []
    for red_value, nir_value in zip(red, nir, strict=True):
        denominator = nir_value + red_value
        values.append(0.0 if denominator == 0 else (nir_value - red_value) / denominator)
    return tuple(values)
