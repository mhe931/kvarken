import pytest

from kvarken_eo.raster import process_scene_window


def test_process_scene_window_downsamples_aligned_bands_and_ndvi():
    bands = {
        "B04": ((1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0)),
        "B08": ((3.0, 3.0, 3.0, 3.0), (3.0, 3.0, 3.0, 3.0)),
    }

    result = process_scene_window(bands, (20.5, 62.8, 22.5, 63.8), (0, 0, 2, 4), 2)

    assert result.red == ((1.0, 1.0),)
    assert result.nir == ((3.0, 3.0),)
    assert result.ndvi[0] == pytest.approx((0.5, 0.5))
    assert result.transform.pixel_to_wgs84(2, 1) == pytest.approx((21.5, 63.3))


def test_process_scene_window_uses_actual_edge_blocks():
    bands = {
        "B04": ((1.0, 2.0, 3.0), (1.0, 2.0, 3.0), (1.0, 2.0, 3.0)),
        "B08": ((2.0, 4.0, 6.0), (2.0, 4.0, 6.0), (2.0, 4.0, 6.0)),
    }

    result = process_scene_window(bands, (20.5, 62.8, 22.5, 63.8), (1, 1, 2, 2), 2)

    assert result.red == ((2.5,),)
    assert result.nir == ((5.0,),)
    assert result.ndvi[0] == pytest.approx((1 / 3,))


def test_process_scene_window_rejects_missing_or_out_of_bounds_windows():
    bands = {"B04": ((1.0, 2.0),), "B08": ((2.0, 4.0),)}
    with pytest.raises(KeyError, match="B08"):
        process_scene_window({"B04": bands["B04"]}, (20.5, 62.8, 22.5, 63.8), (0, 0, 1, 1), 1)
    with pytest.raises(ValueError, match="fit"):
        process_scene_window(bands, (20.5, 62.8, 22.5, 63.8), (0, 1, 1, 2), 1)
