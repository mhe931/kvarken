"""Command-line demo for the offline vertical slice."""

import argparse
import asyncio
import json
import tempfile
import time
from pathlib import Path

from .catalog import SpatialCatalog
from .concurrent import ConcurrentEOIngestor
from .ingestion import AsyncIngestor
from .provenance import FileProvenanceSink
from .reports import generate_experiment_report
from .runner import prune_live_experiment_artifacts, run_live_experiment
from .source import MockEODataSource
from .spatial import KVARKEN_REGION_BBOX
from .transform import transform_stac_to_scene


def _verify_health() -> int:
    fixture = Path(__file__).parents[2] / "tests" / "fixtures" / "stac_search_page_1.json"
    import json

    item = json.loads(fixture.read_text(encoding="utf-8"))["features"][0]
    scene = transform_stac_to_scene(item)
    with tempfile.TemporaryDirectory(prefix="kvarken-health-") as directory:
        root = Path(directory)
        sink = FileProvenanceSink(root / "provenance")
        sink.store(
            source_id=scene.scene_id,
            collection=item["collection"],
            source_uri="fixture://stac_search_page_1",
            payload=item,
        )
        with SpatialCatalog(root / "catalog.sqlite") as catalog:
            catalog.index_scene(scene)
            matches = catalog.query_scenes(roi=KVARKEN_REGION_BBOX)
            removed = catalog.prune_older_than(scene.acquired_at.replace(year=2020))
            catalog.vacuum()
            payloads = sink.prune_raw_payloads(catalog, dry_run=True)
    if len(matches) != 1 or removed != 0 or payloads:
        print("health check failed")
        return 1
    print("health check passed: ingest, provenance, catalog query, retention, and vacuum")
    return 0


def _benchmark_report(output_dir: Path, scenes_count: int, concurrency: int) -> int:
    if scenes_count < 1 or concurrency < 1:
        raise ValueError("scenes-count and concurrency must be positive")
    fixture = Path(__file__).parents[2] / "tests" / "fixtures" / "stac_search_page_1.json"
    template = json.loads(fixture.read_text(encoding="utf-8"))["features"][0]
    items = []
    from .stac import STACItem

    for index in range(scenes_count):
        item = json.loads(json.dumps(template))
        item["id"] = f"benchmark-{index}"
        items.append(
            STACItem(
                item["id"],
                item["collection"],
                "fixture://benchmark",
                item["properties"],
                item,
            )
        )

    class OfflineAdapter:
        async def search(self, **kwargs: object) -> list[STACItem]:
            return items

    with tempfile.TemporaryDirectory(prefix="kvarken-benchmark-") as directory:
        root = Path(directory)
        sink = FileProvenanceSink(root / "provenance")
        with SpatialCatalog(root / "catalog.sqlite") as catalog:
            ingestor = ConcurrentEOIngestor(
                OfflineAdapter(),
                sink,
                max_workers=concurrency,
                catalog=catalog,
            )
            results, metrics = asyncio.run(ingestor.ingest_with_metrics(items))
            started = time.perf_counter()
            catalog.query_scenes(roi=KVARKEN_REGION_BBOX)
            latency_ms = (time.perf_counter() - started) * 1000
            report, _ = generate_experiment_report(
                metrics,
                catalog,
                spatial_query_latency_ms=latency_ms,
                output_dir=output_dir,
            )
    print(
        f"benchmark report written: {report['metrics']['scenes_ingested']} scenes, "
        f"{report['metrics']['throughput_items_per_second']:.2f} items/sec"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true", help="ingest one offline sample scene")
    parser.add_argument(
        "command",
        nargs="?",
        choices=(
            "verify-health",
            "benchmark-report",
            "live-experiment",
            "prune-live-artifacts",
        ),
        help="run an offline end-to-end repository health check",
    )
    parser.add_argument("--output-dir", type=Path, default=Path("reports"))
    parser.add_argument("--scenes-count", type=int, default=100)
    parser.add_argument("--concurrency", type=int, default=4)
    parser.add_argument("--retention-days", type=int, default=30)
    parser.add_argument("--apply", action="store_true", help="delete selected live artifacts")
    args = parser.parse_args(argv)
    if args.command == "verify-health":
        return _verify_health()
    if args.command == "benchmark-report":
        return _benchmark_report(args.output_dir, args.scenes_count, args.concurrency)
    if args.command == "live-experiment":
        path = run_live_experiment(
            args.output_dir,
            limit=args.scenes_count,
            concurrency=args.concurrency,
        )
        print(f"live experiment report written: {path}")
        return 0
    if args.command == "prune-live-artifacts":
        removed = prune_live_experiment_artifacts(
            args.output_dir,
            retention_days=args.retention_days,
            dry_run=not args.apply,
        )
        action = "would remove" if not args.apply else "removed"
        print(f"{action} {len(removed)} live artifact files")
        return 0
    if args.demo:
        result = asyncio.run(
            AsyncIngestor(
                MockEODataSource(
                    {
                        "kvarken-demo-001": {
                            "scene_id": "kvarken-demo-001",
                            "platform": "SENTINEL-2",
                            "acquired_at": "2026-09-14T12:00:00+00:00",
                            "cloud_cover": 12.5,
                            "footprint": [(21.0, 63.0), (21.1, 63.0), (21.1, 63.1)],
                        }
                    }
                )
            ).ingest("kvarken-demo-001")
        )
        print(f"ingested {result.scene.scene_id} in {result.attempts} attempt(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
