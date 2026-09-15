"""Environment-aware live-provider experiment execution."""

import asyncio
import json
import os
import tempfile
import time
from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

from .catalog import SpatialCatalog
from .cdse import CDSEClient, CDSETokenProvider
from .concurrent import ConcurrentEOIngestor
from .provenance import FileProvenanceSink
from .raster import process_scene_window
from .reports import generate_experiment_report
from .stac import STACItem


@dataclass(frozen=True, slots=True)
class CDSESettings:
    token_url: str
    client_id: str
    client_secret: str
    stac_url: str


def prune_live_experiment_artifacts(
    output_dir: Path | str,
    *,
    retention_days: int,
    now: date | None = None,
    dry_run: bool = True,
) -> list[Path]:
    """List or remove dated live artifacts older than the retention window."""
    if retention_days < 0:
        raise ValueError("retention_days must be non-negative")
    directory = Path(output_dir)
    cutoff = (now or datetime.now(UTC).date()) - timedelta(days=retention_days)
    candidates: dict[str, list[Path]] = {}
    for path in directory.glob("experiment_report_live_*.json"):
        suffix = path.stem.removeprefix("experiment_report_live_")
        try:
            artifact_date = datetime.strptime(suffix, "%Y%m%d").date()
        except ValueError:
            continue
        if artifact_date < cutoff:
            candidates.setdefault(suffix, []).append(path)
            markdown = directory / f"experiment_report_live_{suffix}.md"
            if markdown.exists():
                candidates[suffix].append(markdown)
    selected = [path for paths in candidates.values() for path in paths]
    if not dry_run:
        for path in selected:
            path.unlink()
    return selected


def resolve_cdse_settings(environ: Mapping[str, str] | None = None) -> CDSESettings | None:
    values = environ or os.environ
    names = ("CDSE_TOKEN_URL", "CDSE_CLIENT_ID", "CDSE_CLIENT_SECRET", "CDSE_STAC_URL")
    resolved = [values.get(name, "").strip() for name in names]
    return CDSESettings(*resolved) if all(resolved) else None


class OfflineExperimentAdapter:
    def __init__(self, fixture: Path) -> None:
        self._fixture = fixture

    async def search(self, **kwargs: object) -> list[STACItem]:
        del kwargs
        payload = json.loads(self._fixture.read_text(encoding="utf-8"))
        return [
            STACItem(
                item["id"],
                item["collection"],
                f"fixture://{self._fixture.name}",
                item["properties"],
                item,
            )
            for item in payload["features"]
        ]


def _distribution(items: list[STACItem]) -> dict[str, object]:
    collections = Counter(item.collection for item in items)
    platforms = Counter(str(item.properties.get("platform", "unknown")) for item in items)
    cloud_buckets = Counter(_cloud_bucket(item.properties.get("eo:cloud_cover")) for item in items)
    return {
        "collections": dict(sorted(collections.items())),
        "platforms": dict(sorted(platforms.items())),
        "cloud_cover_buckets": dict(sorted(cloud_buckets.items())),
    }


def _cloud_bucket(value: object) -> str:
    try:
        cloud_cover = float(value)
    except (TypeError, ValueError):
        return "unknown"
    if cloud_cover <= 10:
        return "0-10"
    if cloud_cover <= 50:
        return "10-50"
    return "50-100"


def _window_telemetry(item_count: int) -> dict[str, object]:
    """Run a deterministic spectral-window slice and record operational telemetry."""
    if item_count < 1:
        raise ValueError("item_count must be positive")
    import tracemalloc

    bands = {
        "B04": tuple(tuple(0.2 + column / 1000 for column in range(32)) for _ in range(32)),
        "B08": tuple(tuple(0.5 + column / 1000 for column in range(32)) for _ in range(32)),
    }
    started = time.perf_counter()
    tracemalloc.start()
    last_ndvi = 0.0
    for _ in range(item_count):
        result = process_scene_window(
            bands,
            (20.5, 62.8, 22.5, 63.8),
            (4, 4, 16, 16),
            2,
        )
        last_ndvi = result.ndvi[0][0]
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    elapsed = time.perf_counter() - started
    return {
        "windows_processed": item_count,
        "window_shape": [16, 16],
        "downsample_factor": 2,
        "output_shape": [8, 8],
        "elapsed_seconds": round(elapsed, 6),
        "throughput_windows_per_second": round(item_count / elapsed if elapsed else 0.0, 6),
        "peak_memory_bytes": peak_memory,
        "sample_ndvi": round(last_ndvi, 6),
    }


async def _run(
    settings: CDSESettings | None,
    fixture: Path,
    output_dir: Path,
    limit: int,
    concurrency: int,
    run_date: datetime,
) -> Path:
    if limit < 1 or concurrency < 1:
        raise ValueError("limit and concurrency must be positive")
    mode = "live" if settings else "offline-fallback"
    adapter = (
        CDSEClient(
            settings.stac_url,
            CDSETokenProvider(settings.token_url, settings.client_id, settings.client_secret),
        )
        if settings
        else OfflineExperimentAdapter(fixture)
    )
    started = time.perf_counter()
    items = await adapter.search(
        collections=("sentinel-2-l2a",),
        bbox=(20.5, 62.8, 22.5, 63.8),
        limit=limit,
    )
    query_elapsed = time.perf_counter() - started
    items = items[:limit]
    date_string = run_date.astimezone(UTC).strftime("%Y%m%d")
    await asyncio.to_thread(output_dir.mkdir, parents=True, exist_ok=True)
    json_path = output_dir / f"experiment_report_live_{date_string}.json"
    markdown_path = output_dir / f"experiment_report_live_{date_string}.md"
    if json_path.exists() or markdown_path.exists():
        raise FileExistsError(f"dated experiment artifact already exists: {date_string}")
    with tempfile.TemporaryDirectory(prefix="kvarken-live-run-") as directory:
        root = Path(directory)
        sink = FileProvenanceSink(root / "provenance")
        with SpatialCatalog(root / "catalog.sqlite") as catalog:
            ingestor = ConcurrentEOIngestor(adapter, sink, max_workers=concurrency, catalog=catalog)
            results, metrics = await ingestor.ingest_with_metrics(items)
            report, _ = generate_experiment_report(
                metrics,
                catalog,
                spatial_query_latency_ms=query_elapsed * 1000,
                output_dir=root / "report",
            )
            report["run"] = {
                "date": date_string,
                "mode": mode,
                "provider": "CDSE" if settings else "offline-fixture",
                "items_requested": limit,
                "items_returned": len(items),
                "response_distribution": _distribution(items),
            }
            report["network"] = {
                "search_elapsed_seconds": round(query_elapsed, 6),
                "search_round_trip_ms": round(query_elapsed * 1000, 6),
            }
            report["derived"]["quality_profiled_scenes"] = len(results)
            report["window_telemetry"] = _window_telemetry(len(results))
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown = "\n".join(
        [
            "# EO Pipeline Live Experiment Report",
            "",
            f"- Run date: `{date_string}`",
            f"- Mode: `{mode}`",
            f"- Provider: `{report['run']['provider']}`",
            f"- Items returned: `{len(items)}`",
            f"- Search round-trip (ms): `{query_elapsed * 1000:.6f}`",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| Scenes ingested | {report['metrics']['scenes_ingested']} |",
            f"| Throughput (items/sec) | {report['metrics']['throughput_items_per_second']:.6f} |",
            f"| Mean cloud cover | {report['quality']['mean_cloud_cover']:.6f} |",
            f"| Usable scene ratio | {report['quality']['usable_scene_ratio']:.6f} |",
            f"| Search round-trip (ms) | {query_elapsed * 1000:.6f} |",
            f"| Windows processed | {report['window_telemetry']['windows_processed']} |",
            f"| Window throughput (windows/sec) | "
            f"{report['window_telemetry']['throughput_windows_per_second']:.6f} |",
            f"| Window peak memory (bytes) | {report['window_telemetry']['peak_memory_bytes']} |",
            "",
        ]
    )
    markdown_path.write_text(markdown, encoding="utf-8")
    return json_path


def run_live_experiment(
    output_dir: Path | str,
    *,
    limit: int = 25,
    concurrency: int = 4,
    environ: Mapping[str, str] | None = None,
    now: datetime | None = None,
    fixture: Path | None = None,
) -> Path:
    fixture_path = (
        fixture or Path(__file__).parents[2] / "tests" / "fixtures" / "stac_search_page_1.json"
    )
    return asyncio.run(
        _run(
            resolve_cdse_settings(environ),
            fixture_path,
            Path(output_dir),
            limit,
            concurrency,
            now or datetime.now(UTC),
        )
    )
