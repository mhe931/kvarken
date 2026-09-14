from datetime import UTC, datetime, timedelta
from time import perf_counter

from kvarken_eo import EOScene, SpatialCatalog


def test_catalog_query_benchmark_over_thousand_scenes(tmp_path):
    catalog = SpatialCatalog(tmp_path / "benchmark.sqlite")
    scenes = []
    for index in range(1200):
        x = 20.0 + (index % 60) * 0.04
        y = 62.5 + (index % 20) * 0.04
        bbox = (x, y, x + 0.02, y + 0.02)
        scenes.append(
            EOScene(
                f"benchmark-{index}",
                "sentinel-2",
                datetime(2026, 1, 1, tzinfo=UTC) + timedelta(minutes=index),
                5.0,
                ((x, y), (x + 0.02, y), (x + 0.02, y + 0.02), (x, y + 0.02)),
                bbox,
            )
        )
    catalog.index_scenes(scenes)
    start = perf_counter()
    results = catalog.query_scenes(roi=(20.8, 62.8, 21.2, 63.2))
    elapsed_ms = (perf_counter() - start) * 1000
    catalog.close()

    assert results
    assert elapsed_ms < 1000
