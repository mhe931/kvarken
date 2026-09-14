"""Deterministic experiment and benchmark report generation."""

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .catalog import SpatialCatalog
from .concurrent import IngestionMetrics


def generate_experiment_report(
    metrics: IngestionMetrics,
    catalog: SpatialCatalog,
    *,
    spatial_query_latency_ms: float,
    output_dir: Path | str,
) -> tuple[dict[str, Any], str]:
    """Write deterministic JSON and Markdown artifacts for one experiment."""
    catalog_size = len(catalog.scene_ids())
    recovery_ratio = (
        (metrics.scenes_ingested - metrics.failure_count) / metrics.scenes_ingested
        if metrics.scenes_ingested
        else 1.0
    )
    report: dict[str, Any] = {
        "schema_version": 1,
        "metrics": asdict(metrics),
        "catalog": {"scene_count": catalog_size},
        "spatial_query": {"latency_ms": round(spatial_query_latency_ms, 6)},
        "derived": {
            "failure_recovery_ratio": round(recovery_ratio, 6),
            "payload_megabytes": round(metrics.payload_bytes / 1_000_000, 6),
        },
    }
    markdown = _markdown_report(report)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "experiment_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (destination / "experiment_report.md").write_text(markdown, encoding="utf-8")
    return report, markdown


def _markdown_report(report: dict[str, Any]) -> str:
    metrics = report["metrics"]
    derived = report["derived"]
    return "\n".join(
        [
            "# EO Pipeline Experiment Report",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| Scenes ingested | {metrics['scenes_ingested']} |",
            f"| Elapsed seconds | {metrics['elapsed_seconds']:.6f} |",
            f"| Throughput (items/sec) | {metrics['throughput_items_per_second']:.6f} |",
            f"| Failures | {metrics['failure_count']} |",
            f"| Retries | {metrics['retry_count']} |",
            f"| Payload bytes | {metrics['payload_bytes']} |",
            f"| Catalog scenes | {report['catalog']['scene_count']} |",
            f"| Spatial query latency (ms) | {report['spatial_query']['latency_ms']:.6f} |",
            f"| Failure recovery ratio | {derived['failure_recovery_ratio']:.6f} |",
            f"| Payload megabytes | {derived['payload_megabytes']:.6f} |",
            "",
        ]
    )
