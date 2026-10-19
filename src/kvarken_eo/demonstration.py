"""Replay captured STAC metadata and retain evidence; never infer a cloud deployment."""

import argparse
import asyncio
import hashlib
import json
import platform
import subprocess
import threading
import time
from dataclasses import asdict, replace
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import urlopen

from .api import create_catalog_server
from .catalog import SpatialCatalog
from .concurrent import ConcurrentEOIngestor
from .provenance import FileProvenanceSink
from .spatial import KVARKEN_REGION_BBOX, validate_bbox
from .stac import STACClient
from .transform import transform_stac_to_scene


def run_demonstration(
    input_path: Path,
    output_dir: Path,
    *,
    source_uri: str,
    concurrency: int = 4,
) -> dict:
    """Validate a captured page, persist it, reopen the catalog, and probe a local API."""
    if concurrency < 1:
        raise ValueError("concurrency must be positive")
    source = urlsplit(source_uri)
    if (
        source.scheme not in {"https", "fixture", "capture"}
        or not source.netloc
        or source.username
        or source.password
        or source.query
        or source.fragment
    ):
        raise ValueError(
            "source_uri must be a public HTTPS, fixture or capture URI without credentials/query"
        )
    started_at = datetime.now(UTC)
    started = time.perf_counter()
    raw = input_path.read_bytes()
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError("input must be a STAC FeatureCollection")
    items = STACClient._parse_items(payload, source_uri)
    for index, item in enumerate(items):
        for link in item.raw_payload.get("links", []):
            if link.get("rel") == "self":
                original = link.get("href", "")
                parts = urlsplit(original)
                if (
                    parts.scheme != "https"
                    or not parts.netloc
                    or parts.query
                    or parts.fragment
                    or parts.username
                    or parts.password
                ):
                    raise ValueError("STAC self link must be a public unsigned HTTPS URI")
                items[index] = replace(item, source_uri=original)
                break
    if not items:
        raise ValueError("input must contain at least one feature")
    expected_ids = sorted(item.item_id for item in items)
    if len(set(expected_ids)) != len(expected_ids):
        raise ValueError("input contains duplicate scene identifiers")
    for item in items:
        scene = transform_stac_to_scene(item.raw_payload)
        if scene.epsg != 4326:
            raise ValueError(
                "replay requires EPSG:4326 scene metadata; no reprojection is performed"
            )
        if scene.bbox is not None:
            validate_bbox(scene.bbox)
        if any(not (-180 <= lon <= 180 and -90 <= lat <= 90) for lon, lat in scene.footprint):
            raise ValueError("footprint contains invalid geographic coordinates")
    repository = Path(__file__).resolve().parents[2]
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repository, check=True, capture_output=True, text=True
    ).stdout.strip()
    dirty = bool(
        subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repository,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    )
    output_dir.mkdir(parents=True, exist_ok=False)
    (output_dir / "input.json").write_bytes(raw)
    sink = FileProvenanceSink(output_dir / "provenance")
    catalog_path = output_dir / "catalog.sqlite"
    with SpatialCatalog(catalog_path) as catalog:
        ingestor = ConcurrentEOIngestor(
            STACClient("https://example.invalid"), sink, max_workers=concurrency, catalog=catalog
        )
        results, metrics = asyncio.run(ingestor.ingest_with_metrics(items))
    for result in results:
        stored = json.loads(
            (output_dir / "provenance" / result.provenance.raw_payload_path).read_text("utf-8")
        )
        canonical = json.dumps(stored, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        if hashlib.sha256(canonical.encode()).hexdigest() != result.provenance.payload_sha256:
            raise RuntimeError("stored provenance checksum differs from the ingestion record")
    with SpatialCatalog(catalog_path) as catalog:
        reopened_ids = sorted(catalog.scene_ids())
        if reopened_ids != expected_ids:
            raise RuntimeError("reopened catalog does not contain exactly the input scenes")
        region_ids = sorted(
            scene.scene_id for scene in catalog.query_scenes(roi=KVARKEN_REGION_BBOX)
        )
        server = create_catalog_server(catalog)
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        try:
            base_url = f"http://127.0.0.1:{server.server_port}"
            with urlopen(base_url + "/api/health", timeout=10) as response:
                health = json.load(response)
            with urlopen(base_url + "/api/scenes", timeout=10) as response:
                api_ids = sorted(scene["scene_id"] for scene in json.load(response)["scenes"])
            if health != {"status": "ok"} or api_ids != expected_ids:
                raise RuntimeError("API responses do not match the persisted input scenes")
        finally:
            server.shutdown()
            thread.join()
            server.server_close()
    records = [
        json.loads(line)
        for line in (output_dir / "provenance" / "manifest.jsonl").read_text("utf-8").splitlines()
    ]
    if sorted(record["source_id"] for record in records) != expected_ids:
        raise RuntimeError("provenance manifest does not contain exactly the input scenes")
    output_checksums = {
        path.relative_to(output_dir).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(output_dir.rglob("*"))
        if path.is_file()
    }
    report = {
        "schema_version": 1,
        "workload": "metadata-catalog-replay",
        "limitations": [
            "No satellite raster download, decoding, calibration, classification, or validation.",
            "A captured page is replayed; pagination and provider network speed are not measured.",
            "Host information is not proof of CSC project or cPouta provenance.",
            "Missing eo:cloud_cover uses the baseline model default; it is not an observation.",
        ],
        "started_at": started_at.isoformat(),
        "completed_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": time.perf_counter() - started,
        "source_revision": {"sha": revision, "dirty": dirty},
        "source_sha256": {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(Path(__file__).parent.glob("*.py"))
        },
        "environment": {
            "provider": "not-verified",
            "host": platform.node(),
            "platform": platform.platform(),
            "python": platform.python_version(),
        },
        "input": {
            "source_uri": source_uri,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
        },
        "concurrency": concurrency,
        "metrics": asdict(metrics),
        "validation": {
            "catalog_reopened": True,
            "scene_ids": reopened_ids,
            "kvarken_scene_ids": region_ids,
            "api_health": health,
            "api_scene_ids": api_ids,
            "provenance_records": len(records),
        },
        "output_sha256": output_checksums,
    }
    (output_dir / "run.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", "utf-8"
    )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, dest="input_path")
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--source-uri", required=True)
    parser.add_argument("--concurrency", type=int, default=4)
    args = parser.parse_args()
    report = run_demonstration(**vars(args))
    print(
        f"metadata replay verified: {report['metrics']['scenes_ingested']} scenes; "
        f"environment provider remains {report['environment']['provider']}"
    )


if __name__ == "__main__":
    main()
