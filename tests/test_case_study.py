from urllib.error import HTTPError

import pytest

np = pytest.importorskip("numpy")
rio = pytest.importorskip("rasterio")

from rasterio.enums import Resampling  # noqa: E402
from rasterio.transform import from_origin  # noqa: E402

from kvarken_eo import case_study  # noqa: E402
from kvarken_eo.case_study import (  # noqa: E402
    AssetSigner,
    Grid,
    optical_mosaic,
    read_aligned,
    read_class_fraction,
    write_raster,
)


def test_alignment_averages_linear_power_and_preserves_nodata(tmp_path):
    source = tmp_path / "source.tif"
    values = np.array([[1, 100, -32768, -32768], [1, 100, -32768, -32768]] * 2, dtype="float32")
    with rio.open(
        source,
        "w",
        driver="GTiff",
        height=4,
        width=4,
        count=1,
        dtype="float32",
        crs="EPSG:32634",
        transform=from_origin(400000, 7000000, 100, 100),
        nodata=-32768,
    ) as dst:
        dst.write(values, 1)
    grid = Grid(from_origin(400000, 7000000, 200, 200), 2, 2, "EPSG:32634")
    result, metadata = read_aligned(str(source), grid, Resampling.average)
    np.testing.assert_allclose(result[:, 0], 50.5)
    assert np.isnan(result[:, 1]).all()
    assert metadata["crs"] == "EPSG:32634"
    assert metadata["nodata"] == -32768


def test_saved_raster_retains_grid_values_units_and_nodata(tmp_path):
    grid = Grid(from_origin(400000, 7000000, 100, 100), 3, 2, "EPSG:32634")
    values = np.array([[1, 2, np.nan], [3, 4, 5]], dtype="float32")
    path = tmp_path / "data.tif"
    write_raster(path, values, grid, "linear gamma0")
    with rio.open(path) as src:
        assert src.crs.to_epsg() == 32634
        assert src.transform == grid.transform
        assert src.descriptions == ("linear gamma0",)
        assert np.isnan(src.nodata)
        np.testing.assert_allclose(src.read(1), values, equal_nan=True)


def test_grid_clips_original_roi_and_bounds_memory():
    grid = Grid.for_bbox((20.5, 62.8, 22.5, 63.8), 100)
    assert grid.width * grid.height < 2_000_000
    assert grid.crs == "EPSG:32634"
    with pytest.raises(ValueError, match="resolution"):
        Grid.for_bbox((20.5, 62.8, 22.5, 63.8), 0)
    with pytest.raises(ValueError, match="bounded"):
        Grid.for_bbox((0, 0, 60, 70), 10)


def test_asset_signer_reuses_container_token_without_persisting_or_repeated_requests():
    requests = []

    def fetch(url):
        requests.append(url)
        return {"token": "se=2099-01-01T00%3A00%3A00Z&sig=test-only"}

    signer = AssetSigner(fetch)
    first = signer.sign("https://test.blob.core.windows.net/data/vv.tif")
    second = signer.sign("https://test.blob.core.windows.net/data/vh.tif")
    assert first.endswith("sig=test-only")
    assert second.endswith("sig=test-only")
    assert len(requests) == 1
    with pytest.raises(ValueError, match="unsigned"):
        signer.sign(first)


def test_json_download_retries_429_but_not_schema_failures(monkeypatch):
    attempts = []
    sleeps = []

    def throttled(url, timeout):
        attempts.append(url)
        raise HTTPError(url, 429, "rate limit", {"Retry-After": "2"}, None)

    monkeypatch.setattr(case_study, "urlopen", throttled)
    monkeypatch.setattr(case_study.time, "sleep", sleeps.append)
    with pytest.raises(HTTPError):
        case_study._json_url("https://example.invalid/public-json")
    assert len(attempts) == 3
    assert sleeps == [2.0, 2.0]


def test_optical_mosaic_uses_one_common_source_tile_for_all_bands():
    arrays = {}
    for index, values in enumerate(([0, 2, 3, 6], [4, 5, 6, 11])):
        for band, value in zip(("B03", "B08", "B11", "SCL"), values, strict=True):
            arrays[f"optical_{index}_{band}.tif"] = np.array([[value]], dtype=float)
    mosaic = optical_mosaic(arrays, (1, 1))
    assert [mosaic[band][0, 0] for band in ("B03", "B08", "B11", "SCL")] == [4, 5, 6, 11]


def test_native_class_fraction_detects_land_missed_by_nearest_sampling(tmp_path):
    path = tmp_path / "mask.tif"
    native = np.full((4, 4), 80, dtype="uint8")
    native[0, 0] = 10
    with rio.open(
        path,
        "w",
        driver="GTiff",
        height=4,
        width=4,
        count=1,
        dtype="uint8",
        crs="EPSG:32634",
        transform=from_origin(400000, 7000000, 10, 10),
        nodata=0,
    ) as dst:
        dst.write(native, 1)
    grid = Grid(from_origin(400000, 7000000, 20, 20), 2, 2, "EPSG:32634")
    fraction = read_class_fraction(str(path), grid, 80)
    assert fraction[0, 0] == pytest.approx(0.75)
    np.testing.assert_allclose(fraction[1], 1)
