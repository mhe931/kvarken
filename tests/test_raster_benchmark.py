from kvarken_eo.raster import benchmark_downsample, downsample_scene_bands


def test_multiscale_scene_benchmark_has_stable_work_metrics():
    scene = {
        "B04": tuple(tuple(float(column) for column in range(64)) for _ in range(64)),
        "B08": tuple(tuple(float(column + 10) for column in range(64)) for _ in range(64)),
    }

    reduced = downsample_scene_bands(scene, 4)
    benchmark = benchmark_downsample(scene["B04"], 4)

    assert set(reduced) == {"B04", "B08"}
    assert all(len(row) == 16 for row in reduced["B04"])
    assert len(reduced["B04"]) == 16
    assert reduced["B08"][0][0] == reduced["B04"][0][0] + 10
    assert benchmark.input_pixels == 4096
    assert benchmark.output_pixels == 256
    assert benchmark.throughput_pixels_per_second > 0
    assert benchmark.peak_memory_bytes > 0
