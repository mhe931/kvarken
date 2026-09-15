import pytest

from kvarken_eo.raster import (
    AffineGridTransform,
    benchmark_downsample,
    downsample_band,
)


def test_downsample_preserves_block_mean_brightness():
    band = ((10.0, 20.0, 30.0, 40.0), (20.0, 30.0, 40.0, 50.0))

    assert downsample_band(band, 2) == ((20.0, 40.0),)


def test_downsample_handles_partial_edge_blocks_without_darkening():
    band = ((1.0, 2.0, 3.0), (4.0, 5.0, 6.0), (7.0, 8.0, 9.0))

    assert downsample_band(band, 2) == ((3.0, 4.5), (7.5, 9.0))


def test_downsample_rejects_invalid_or_ragged_bands():
    with pytest.raises(ValueError, match="positive"):
        downsample_band(((1.0,),), 0)
    with pytest.raises(ValueError, match="equal lengths"):
        downsample_band(((1.0,), (1.0, 2.0)), 2)


def test_affine_grid_transform_round_trips_wgs84_coordinates():
    transform = AffineGridTransform.from_bbox((20.5, 62.8, 22.5, 63.8), 200, 100)

    coordinate = transform.pixel_to_wgs84(75.5, 24.5)

    assert transform.wgs84_to_pixel(*coordinate) == pytest.approx((75.5, 24.5))


def test_affine_grid_transform_rejects_invalid_geometry():
    with pytest.raises(ValueError, match="dimensions"):
        AffineGridTransform.from_bbox((20.5, 62.8, 22.5, 63.8), 0, 100)
    with pytest.raises(ValueError, match="less than"):
        AffineGridTransform.from_bbox((22.5, 62.8, 20.5, 63.8), 100, 100)


def test_downsample_benchmark_reports_work_and_memory():
    band = tuple(tuple(float(i) for i in range(32)) for _ in range(32))
    benchmark = benchmark_downsample(band, 2)

    assert benchmark.input_pixels == 1024
    assert benchmark.output_pixels == 256
    assert benchmark.elapsed_seconds >= 0
    assert benchmark.throughput_pixels_per_second > 0
    assert benchmark.peak_memory_bytes > 0
