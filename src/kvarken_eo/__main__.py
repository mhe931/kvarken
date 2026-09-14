"""Command-line demo for the offline vertical slice."""

import argparse
import asyncio
import tempfile
from pathlib import Path

from .catalog import SpatialCatalog
from .ingestion import AsyncIngestor
from .provenance import FileProvenanceSink
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true", help="ingest one offline sample scene")
    parser.add_argument(
        "command",
        nargs="?",
        choices=("verify-health",),
        help="run an offline end-to-end repository health check",
    )
    args = parser.parse_args(argv)
    if args.command == "verify-health":
        return _verify_health()
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
