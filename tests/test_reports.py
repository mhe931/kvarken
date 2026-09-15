import json

from kvarken_eo import IngestionMetrics, SpatialCatalog, generate_experiment_report
from kvarken_eo.__main__ import main


def test_report_writes_deterministic_json_and_markdown(tmp_path):
    catalog = SpatialCatalog(tmp_path / "catalog.sqlite")
    metrics = IngestionMetrics(10, 2.0, 5.0, 1, 2, 2_000_000)

    report, markdown = generate_experiment_report(
        metrics,
        catalog,
        spatial_query_latency_ms=1.25,
        output_dir=tmp_path / "reports",
    )
    catalog.close()

    assert report["catalog"]["scene_count"] == 0
    assert report["derived"]["failure_recovery_ratio"] == 0.9
    assert report["derived"]["payload_megabytes"] == 2.0
    assert report["quality"]["usable_scene_count"] == 0
    assert report["quality"]["mean_cloud_cover"] == 0.0
    loaded = json.loads((tmp_path / "reports" / "experiment_report.json").read_text())
    assert loaded == report
    assert "| Throughput (items/sec) | 5.000000 |" in markdown
    assert (tmp_path / "reports" / "experiment_report.md").exists()


def test_benchmark_report_cli_parameters(tmp_path):
    output = tmp_path / "benchmark"

    assert (
        main(
            [
                "benchmark-report",
                "--output-dir",
                str(output),
                "--scenes-count",
                "3",
                "--concurrency",
                "2",
            ]
        )
        == 0
    )

    report = json.loads((output / "experiment_report.json").read_text())
    assert report["metrics"]["scenes_ingested"] == 3
    assert report["catalog"]["scene_count"] == 3
    assert (output / "experiment_report.md").read_text().startswith("# EO Pipeline")
