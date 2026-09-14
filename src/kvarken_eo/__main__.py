"""Command-line demo for the offline vertical slice."""

import argparse
import asyncio

from .ingestion import AsyncIngestor
from .source import MockEODataSource


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true", help="ingest one offline sample scene")
    args = parser.parse_args()
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


if __name__ == "__main__":
    main()
