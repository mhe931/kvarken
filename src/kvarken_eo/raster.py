"""Small dependency-free raster asset and NDVI helpers."""

import asyncio
import time
import tracemalloc
from collections.abc import Sequence
from dataclasses import dataclass
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


RasterGrid = tuple[tuple[float, ...], ...]
Coordinate = tuple[float, float]


@dataclass(frozen=True, slots=True)
class AffineGridTransform:
    """Map local pixel coordinates to an EPSG:4326 bounding geometry."""

    min_longitude: float
    min_latitude: float
    longitude_per_pixel: float
    latitude_per_pixel: float

    @classmethod
    def from_bbox(
        cls,
        bbox: Sequence[float],
        width: int,
        height: int,
    ) -> "AffineGridTransform":
        if len(bbox) != 4:
            raise ValueError("bbox must contain four coordinates")
        if width <= 0 or height <= 0:
            raise ValueError("grid dimensions must be positive")
        min_longitude, min_latitude, max_longitude, max_latitude = map(float, bbox)
        if min_longitude >= max_longitude or min_latitude >= max_latitude:
            raise ValueError("bbox minimums must be less than maximums")
        return cls(
            min_longitude,
            min_latitude,
            (max_longitude - min_longitude) / width,
            (max_latitude - min_latitude) / height,
        )

    def pixel_to_wgs84(self, column: float, row: float) -> Coordinate:
        return (
            self.min_longitude + column * self.longitude_per_pixel,
            self.min_latitude + row * self.latitude_per_pixel,
        )

    def wgs84_to_pixel(self, longitude: float, latitude: float) -> Coordinate:
        if self.longitude_per_pixel == 0 or self.latitude_per_pixel == 0:
            raise ValueError("grid scale must be non-zero")
        return (
            (longitude - self.min_longitude) / self.longitude_per_pixel,
            (latitude - self.min_latitude) / self.latitude_per_pixel,
        )


def downsample_band(band: Sequence[Sequence[float]], factor: int) -> RasterGrid:
    """Average non-overlapping blocks while preserving mean brightness."""

    if factor <= 0:
        raise ValueError("factor must be positive")
    if not band or not band[0]:
        raise ValueError("band must not be empty")
    width = len(band[0])
    if any(len(row) != width for row in band):
        raise ValueError("band rows must have equal lengths")
    output = []
    for row_start in range(0, len(band), factor):
        output_row = []
        for column_start in range(0, width, factor):
            values = [
                float(band[row][column])
                for row in range(row_start, min(row_start + factor, len(band)))
                for column in range(column_start, min(column_start + factor, width))
            ]
            output_row.append(sum(values) / len(values))
        output.append(tuple(output_row))
    return tuple(output)


@dataclass(frozen=True, slots=True)
class DownsampleBenchmark:
    input_pixels: int
    output_pixels: int
    elapsed_seconds: float
    throughput_pixels_per_second: float
    peak_memory_bytes: int


def benchmark_downsample(
    band: Sequence[Sequence[float]],
    factor: int,
) -> DownsampleBenchmark:
    """Measure downsampling throughput and peak traced Python memory."""

    input_pixels = sum(len(row) for row in band)
    tracemalloc.start()
    started = time.perf_counter()
    result = downsample_band(band, factor)
    elapsed = time.perf_counter() - started
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    output_pixels = sum(len(row) for row in result)
    return DownsampleBenchmark(
        input_pixels,
        output_pixels,
        elapsed,
        input_pixels / elapsed if elapsed else float("inf"),
        peak_memory,
    )


def calculate_ndvi(red: Sequence[float], nir: Sequence[float]) -> tuple[float, ...]:
    """Calculate NDVI values, preserving zero-denominator pixels as 0.0."""

    if len(red) != len(nir):
        raise ValueError("red and nir bands must have equal lengths")
    values = []
    for red_value, nir_value in zip(red, nir, strict=True):
        denominator = nir_value + red_value
        values.append(0.0 if denominator == 0 else (nir_value - red_value) / denominator)
    return tuple(values)
