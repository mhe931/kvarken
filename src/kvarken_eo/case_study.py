"""Optional, sequential, range-read Sentinel-1/optical-reference case study."""

import argparse
import hashlib
import json
import math
import platform
import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from importlib.metadata import version
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlsplit
from urllib.request import urlopen

import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.errors import RasterioIOError
from rasterio.features import geometry_mask
from rasterio.transform import Affine, from_origin
from rasterio.vrt import WarpedVRT
from rasterio.warp import reproject, transform_bounds, transform_geom
from rasterio.windows import Window, from_bounds
from rasterio.windows import bounds as window_bounds

from .demonstration import run_demonstration
from .sea_ice import (
    agreement_metrics,
    buffered_water,
    fit_discriminant,
    optical_reference,
    power_to_db,
    predict_discriminant,
    spatial_partition,
)
from .spatial import validate_bbox

STAC_ROOT = "https://planetarycomputer.microsoft.com/api/stac/v1"


@dataclass(frozen=True)
class Grid:
    transform: Affine
    width: int
    height: int
    crs: str

    @classmethod
    def for_bbox(cls, bbox: tuple, resolution: float) -> "Grid":
        validate_bbox(bbox)
        if not math.isfinite(resolution) or resolution < 10:
            raise ValueError("resolution must be finite and at least 10 metres")
        west, south, east, north = transform_bounds("EPSG:4326", "EPSG:32634", *bbox)
        west = math.floor(west / resolution) * resolution
        north = math.ceil(north / resolution) * resolution
        width = math.ceil((east - west) / resolution)
        height = math.ceil((north - south) / resolution)
        if width * height > 4_000_000:
            raise ValueError("analysis grid must be bounded to four million cells")
        return cls(from_origin(west, north, resolution, resolution), width, height, "EPSG:32634")


def read_aligned(uri: str, grid: Grid, resampling: Resampling) -> tuple[np.ndarray, dict]:
    try:
        with rasterio.Env(
            GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
            GDAL_HTTP_TIMEOUT="60",
            GDAL_HTTP_MAX_RETRY="2",
            GDAL_HTTP_RETRY_DELAY="2",
        ):
            with rasterio.open(uri) as source:
                metadata = {
                    "crs": str(source.crs),
                    "shape": list(source.shape),
                    "nodata": source.nodata,
                    "overviews": source.overviews(1),
                    "tags": source.tags(),
                }
                with WarpedVRT(
                    source,
                    crs=grid.crs,
                    transform=grid.transform,
                    width=grid.width,
                    height=grid.height,
                    dtype="float32",
                    nodata=float("nan"),
                    resampling=resampling,
                ) as vrt:
                    return vrt.read(1), metadata
    except RasterioIOError:
        raise RuntimeError("Raster access failed; no signed asset URL is logged") from None


def write_raster(path: Path, values: np.ndarray, grid: Grid, description: str) -> None:
    if values.shape != (grid.height, grid.width):
        raise ValueError("output raster shape does not match the target grid")
    with rasterio.open(
        path,
        "w",
        driver="GTiff",
        height=grid.height,
        width=grid.width,
        count=1,
        dtype="float32",
        crs=grid.crs,
        transform=grid.transform,
        nodata=float("nan"),
        compress="deflate",
    ) as destination:
        destination.write(values.astype("float32"), 1)
        destination.set_band_description(1, description)


def read_class_fraction(uri: str, grid: Grid, class_value: int) -> np.ndarray:
    """Aggregate native categorical pixels, not a nearest-neighbour overview."""
    result = np.full((grid.height, grid.width), np.nan, dtype="float32")
    try:
        with rasterio.Env(
            GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
            GDAL_HTTP_TIMEOUT="60",
            GDAL_HTTP_MAX_RETRY="2",
            GDAL_HTTP_RETRY_DELAY="2",
        ):
            with rasterio.open(uri) as source:
                for row in range(0, grid.height, 256):
                    for col in range(0, grid.width, 256):
                        window = Window(
                            col, row, min(256, grid.width - col), min(256, grid.height - row)
                        )
                        bounds = transform_bounds(
                            grid.crs, source.crs, *window_bounds(window, grid.transform)
                        )
                        if (
                            bounds[2] <= source.bounds.left
                            or bounds[0] >= source.bounds.right
                            or bounds[3] <= source.bounds.bottom
                            or bounds[1] >= source.bounds.top
                        ):
                            continue
                        native_window = from_bounds(*bounds, source.transform)
                        left = max(0, math.floor(native_window.col_off))
                        top = max(0, math.floor(native_window.row_off))
                        right = min(
                            source.width, math.ceil(native_window.col_off + native_window.width)
                        )
                        bottom = min(
                            source.height, math.ceil(native_window.row_off + native_window.height)
                        )
                        native_window = Window(left, top, right - left, bottom - top)
                        if native_window.width * native_window.height > 20_000_000:
                            raise ValueError("native categorical window exceeds memory bound")
                        native = source.read(1, window=native_window)
                        binary = (native == class_value).astype("float32")
                        destination = np.full(
                            (int(window.height), int(window.width)), np.nan, dtype="float32"
                        )
                        reproject(
                            binary,
                            destination,
                            src_transform=source.window_transform(native_window),
                            src_crs=source.crs,
                            src_nodata=np.nan,
                            dst_transform=rasterio.windows.transform(window, grid.transform),
                            dst_crs=grid.crs,
                            dst_nodata=np.nan,
                            resampling=Resampling.average,
                        )
                        result[row : row + int(window.height), col : col + int(window.width)] = (
                            destination
                        )
    except RasterioIOError:
        raise RuntimeError("Native categorical raster access failed; signed URL withheld") from None
    return result


def optical_mosaic(arrays: dict, shape: tuple) -> dict[str, np.ndarray]:
    bands = ["B03", "B08", "B11", "SCL"]
    if any(name.endswith("_water_fraction.tif") and name.startswith("optical_") for name in arrays):
        bands += ["water_fraction", "ice_fraction"]
    result = {band: np.full(shape, np.nan) for band in bands}
    indexes = sorted({name.split("_")[1] for name in arrays if name.startswith("optical_")})
    for index in indexes:
        tile = {band: arrays[f"optical_{index}_{band}.tif"] for band in bands}
        valid = ~np.isfinite(result["B03"])
        for band, values in tile.items():
            valid &= np.isfinite(values)
            if band in {"B03", "B08", "B11", "SCL"}:
                valid &= values > 0
        for band, values in tile.items():
            result[band][valid] = values[valid]
    return result


def _json_url(url: str) -> dict:
    for attempt in range(3):
        try:
            with urlopen(url, timeout=60) as response:
                result = json.load(response)
            if not isinstance(result, dict):
                raise ValueError("provider JSON must be an object")
            return result
        except HTTPError as error:
            if error.code != 429 or attempt == 2:
                raise
            retry_after = error.headers.get("Retry-After")
            if retry_after is None:
                delay = 2**attempt
            else:
                try:
                    delay = float(retry_after)
                except ValueError:
                    delay = max(
                        0, (parsedate_to_datetime(retry_after) - datetime.now(UTC)).total_seconds()
                    )
            time.sleep(max(0, delay))
        except (TimeoutError, URLError) as error:
            if isinstance(error, URLError) and not isinstance(error.reason, TimeoutError):
                raise
            if attempt == 2:
                raise
            time.sleep(2**attempt)
    raise AssertionError("JSON retry loop must return or raise")


class AssetSigner:
    def __init__(self, fetch: Callable[[str], dict] = _json_url) -> None:
        self._fetch = fetch
        self._tokens: dict[tuple[str, str], tuple[datetime, str]] = {}

    def sign(self, href: str) -> str:
        parts = urlsplit(href)
        if (
            parts.scheme != "https"
            or not parts.hostname
            or not parts.hostname.endswith(".blob.core.windows.net")
        ):
            raise ValueError("only public Planetary Computer Azure assets are supported")
        if parts.query or parts.username or parts.password or parts.fragment:
            raise ValueError("configuration must contain unsigned asset URLs")
        account = parts.hostname.split(".")[0]
        container = parts.path.lstrip("/").split("/")[0]
        key = (account, container)
        cached = self._tokens.get(key)
        if cached is None or (cached[0] - datetime.now(UTC)).total_seconds() < 120:
            payload = self._fetch(
                f"https://planetarycomputer.microsoft.com/api/sas/v1/token/{account}/{container}"
            )
            token = payload["token"]
            expiry = datetime.fromisoformat(parse_qs(token)["se"][0].replace("Z", "+00:00"))
            self._tokens[key] = (expiry, token)
        return href + "?" + self._tokens[key][1]


def _save_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n", "utf-8")


def acquire(config_path: Path, directory: Path, *, resume: bool = False) -> None:
    """Save unsigned source metadata and checksummed, reprojected input windows."""
    config = json.loads(config_path.read_text("utf-8"))
    grid = Grid.for_bbox(tuple(config["bbox"]), config["resolution_m"])
    if resume:
        if (directory / "manifest.json").exists():
            raise FileExistsError("acquisition is already complete; use --reuse-inputs")
        if json.loads((directory / "config.json").read_text("utf-8")) != config:
            raise ValueError("cannot resume acquisition with a different configuration")
    else:
        directory.mkdir(parents=True, exist_ok=False)
        _save_json(directory / "config.json", config)
    signer = AssetSigner()
    scene_items = []
    records = []
    for role, products in (
        ("sar", [config["sar"]]),
        ("optical", config["optical"]),
        ("landcover", config["landcover"]),
    ):
        for product_index, product in enumerate(products):
            url = f"{STAC_ROOT}/collections/{product['collection']}/items/{product['id']}"
            metadata_path = directory / f"{role}_{product_index}_stac.json"
            item = (
                json.loads(metadata_path.read_text("utf-8"))
                if resume and metadata_path.exists()
                else _json_url(url)
            )
            if item.get("id") != product["id"] or item.get("collection") != product["collection"]:
                raise ValueError("provider returned the wrong product identity")
            if not metadata_path.exists():
                _save_json(metadata_path, item)
            if role != "landcover":
                scene_items.append(item)
            for asset in product["assets"]:
                print(f"Reading {role} {product_index + 1}: {asset}", flush=True)
                href = item["assets"][asset]["href"]
                resampling = Resampling.nearest if asset in {"SCL", "map"} else Resampling.average
                filename = f"{role}_{product_index}_{asset}.tif"
                if resume and (directory / filename).exists():
                    with rasterio.open(directory / filename) as cached:
                        if (
                            cached.shape != (grid.height, grid.width)
                            or cached.transform != grid.transform
                            or str(cached.crs) != grid.crs
                        ):
                            raise ValueError("cached input grid does not match the configuration")
                        cached.read(1)
                    sidecar = directory / (filename + ".source.json")
                    metadata = (
                        json.loads(sidecar.read_text("utf-8"))
                        if sidecar.exists()
                        else {"reused_interrupted_window": True, "source_grid": "see STAC"}
                    )
                else:
                    values, metadata = read_aligned(signer.sign(href), grid, resampling)
                    temporary = directory / (filename + ".partial")
                    write_raster(temporary, values, grid, asset)
                    _save_json(directory / (filename + ".source.json"), metadata)
                    temporary.replace(directory / filename)
                records.append(
                    {
                        "role": role,
                        "product_id": product["id"],
                        "acquisition": item["properties"]["datetime"],
                        "collection": product["collection"],
                        "asset": asset,
                        "source_uri": href,
                        "local_window": filename,
                        "source_metadata": metadata,
                        "resampling": resampling.name,
                        "full_original_file_checksum": None,
                    }
                )
    _save_json(
        directory / "scenes.json",
        {"type": "FeatureCollection", "features": scene_items, "links": []},
    )
    checksums = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(directory.iterdir())
        if path.is_file()
    }
    _save_json(
        directory / "manifest.json",
        {
            "downloaded_at": datetime.now(UTC).isoformat(),
            "records": records,
            "sha256": checksums,
            "note": "Checksums identify reprojected windows, not complete original SAFE files.",
        },
    )


def _load_inputs(directory: Path) -> tuple[dict, Grid, dict, dict]:
    manifest = json.loads((directory / "manifest.json").read_text("utf-8"))
    for name, expected in manifest["sha256"].items():
        if Path(name).name != name:
            raise ValueError("manifest paths must be simple filenames")
        if hashlib.sha256((directory / name).read_bytes()).hexdigest() != expected:
            raise ValueError(f"input checksum mismatch: {name}")
    config = json.loads((directory / "config.json").read_text("utf-8"))
    grid = Grid.for_bbox(tuple(config["bbox"]), config["resolution_m"])
    arrays = {}
    for record in manifest["records"]:
        name = record["local_window"]
        if name not in manifest["sha256"]:
            raise ValueError("raster record lacks a verified checksum")
        with rasterio.open(directory / name) as source:
            if (
                source.shape != (grid.height, grid.width)
                or source.transform != grid.transform
                or str(source.crs) != grid.crs
            ):
                raise ValueError("input raster grid differs from the configuration")
            arrays[name] = source.read(1)
    return config, grid, arrays, manifest


def prepare_quality_masks(directory: Path) -> None:
    config, grid, _, _ = _load_inputs(directory)
    target = directory / "quality_masks"
    base_sha = hashlib.sha256((directory / "manifest.json").read_bytes()).hexdigest()
    if target.exists():
        if (target / "manifest.json").exists():
            raise FileExistsError("quality masks already complete; reuse without preparation")
        if json.loads((target / "base.json").read_text("utf-8")) != {"sha256": base_sha}:
            raise ValueError("cannot resume quality masks for different inputs")
    else:
        target.mkdir()
        _save_json(target / "base.json", {"sha256": base_sha})
    signer = AssetSigner()
    records = []
    for role, products, asset, classes in (
        ("landcover", config["landcover"], "map", (("water", 80),)),
        ("optical", config["optical"], "SCL", (("water", 6), ("ice", 11))),
    ):
        for index, _product in enumerate(products):
            item = json.loads((directory / f"{role}_{index}_stac.json").read_text("utf-8"))
            href = item["assets"][asset]["href"]
            signed = signer.sign(href)
            for label, value in classes:
                print(f"Native-resolution coverage: {role} {index + 1} {label}", flush=True)
                name = f"{role}_{index}_{label}_fraction.tif"
                receipt = target / (name + ".json")
                if receipt.exists():
                    if (
                        hashlib.sha256((target / name).read_bytes()).hexdigest()
                        != json.loads(receipt.read_text("utf-8"))["sha256"]
                    ):
                        raise ValueError(f"interrupted quality mask checksum mismatch: {name}")
                else:
                    values = read_class_fraction(signed, grid, value)
                    temporary = target / (name + ".partial")
                    write_raster(temporary, values, grid, f"Native class {value} fraction")
                    temporary.replace(target / name)
                    _save_json(
                        receipt,
                        {"sha256": hashlib.sha256((target / name).read_bytes()).hexdigest()},
                    )
                records.append({"file": name, "source_uri": href, "class_value": value})
    recovered_metadata = {}
    item = json.loads((directory / "sar_0_stac.json").read_text("utf-8"))
    for band in ("vv", "vh"):
        try:
            with rasterio.open(signer.sign(item["assets"][band]["href"])) as source:
                recovered_metadata[band] = {
                    "crs": str(source.crs),
                    "shape": source.shape,
                    "nodata": source.nodata,
                    "tags": source.tags(),
                }
        except RasterioIOError:
            raise RuntimeError("Source metadata access failed; signed URL withheld") from None
    _save_json(
        target / "manifest.json",
        {
            "base_manifest_sha256": hashlib.sha256(
                (directory / "manifest.json").read_bytes()
            ).hexdigest(),
            "created_at": datetime.now(UTC).isoformat(),
            "method": (
                "Native categorical class fractions averaged in bounded windows; no overviews"
            ),
            "records": records,
            "recovered_sar_source_metadata": recovered_metadata,
            "sha256": {
                path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                for path in target.glob("*.tif")
            },
        },
    )


def analyze(directory: Path, output: Path) -> dict:
    started = time.perf_counter()
    started_at = datetime.now(UTC).isoformat()
    config, grid, arrays, manifest = _load_inputs(directory)
    quality_path = directory / "quality_masks" / "manifest.json"
    quality = json.loads(quality_path.read_text("utf-8"))
    if (
        quality["base_manifest_sha256"]
        != hashlib.sha256((directory / "manifest.json").read_bytes()).hexdigest()
    ):
        raise ValueError("quality masks belong to a different input manifest")
    for name, checksum in quality["sha256"].items():
        if Path(name).name != name:
            raise ValueError("quality mask filenames must be simple filenames")
        path = quality_path.parent / name
        if hashlib.sha256(path.read_bytes()).hexdigest() != checksum:
            raise ValueError(f"quality mask checksum mismatch: {name}")
        with rasterio.open(path) as source:
            if (
                source.shape != (grid.height, grid.width)
                or source.transform != grid.transform
                or str(source.crs) != grid.crs
            ):
                raise ValueError("quality mask grid differs from analysis grid")
            arrays[name] = source.read(1)
    output.mkdir(parents=True, exist_ok=False)
    shape = (grid.height, grid.width)
    west, south, east, north = config["bbox"]
    ring = (
        [[x, south] for x in np.linspace(west, east, 40)]
        + [[east, y] for y in np.linspace(south, north, 40)]
        + [[x, north] for x in np.linspace(east, west, 40)]
        + [[west, y] for y in np.linspace(north, south, 40)]
    )
    roi = geometry_mask(
        [transform_geom("EPSG:4326", grid.crs, {"type": "Polygon", "coordinates": [ring]})],
        shape,
        grid.transform,
        invert=True,
    )
    vv, vh = (power_to_db(arrays[f"sar_0_{band}.tif"]) for band in ("vv", "vh"))
    from scipy.ndimage import label

    native_water_fraction = np.fmin.reduce(
        [
            values
            for name, values in arrays.items()
            if name.startswith("landcover_") and name.endswith("_water_fraction.tif")
        ]
    )
    permanent_water = (native_water_fraction >= 0.999999) & roi
    components, _ = label(permanent_water, structure=np.ones((3, 3)))
    counts = np.bincount(components.ravel())
    counts[0] = 0
    if not counts.any():
        raise ValueError("no connected water domain in the study region")
    marine_domain = components == counts.argmax()
    water = (
        buffered_water(
            np.where(marine_domain, 80, 0),
            math.ceil(config["coast_buffer_m"] / config["resolution_m"]),
        )
        & roi
    )
    valid = water & np.isfinite(vv) & np.isfinite(vh)
    optical = optical_mosaic(arrays, shape)
    green, nir, swir = (
        optical[band] / config["optical_quantification"] for band in ("B03", "B08", "B11")
    )
    scl = optical["SCL"]
    reference = optical_reference(green, nir, swir, scl)
    reference[(reference == 0) & (optical["water_fraction"] < 0.99)] = -1
    reference[(reference == 1) & (optical["ice_fraction"] < 0.99)] = -1
    reference[~valid] = -1
    training, testing, blocks = spatial_partition(
        shape,
        int(config["block_m"] / config["resolution_m"]),
        int(config["block_edge_exclusion_m"] / config["resolution_m"]),
    )
    training &= reference >= 0
    testing &= reference >= 0
    if min(np.sum(training & (reference == c)) for c in (0, 1)) < 100:
        raise ValueError(
            "insufficient optical reference support: need 100 training cells per class"
        )
    features = np.stack([vv, vh], axis=-1)
    model = fit_discriminant(features[training], reference[training])
    prediction = np.full(shape, np.nan)
    prediction[valid] = predict_discriminant(features[valid], model)
    metrics = agreement_metrics(reference[testing], prediction[testing])
    pixel_km2 = abs(grid.transform.a * grid.transform.e) / 1_000_000
    block_results = []
    for block in np.unique(blocks[testing]):
        selected = testing & (blocks == block)
        counts = [int(np.sum(selected & (reference == c))) for c in (0, 1)]
        entry = {"block": int(block), "reference_counts": counts}
        entry["metrics"] = agreement_metrics(reference[selected], prediction[selected])
        block_results.append(entry)
    for name, values, description in (
        ("vv_db.tif", np.where(roi, vv, np.nan), "VV gamma0 dB"),
        ("vh_db.tif", np.where(roi, vh, np.nan), "VH gamma0 dB"),
        ("water_mask.tif", water.astype(float), "WorldCover water with coastal exclusion"),
        (
            "optical_reference.tif",
            np.where(reference >= 0, reference, np.nan),
            "0 water; 1 snow ice",
        ),
        ("candidate_ice.tif", prediction, "Exploratory SAR class: 0 water; 1 candidate ice"),
        ("heldout_mask.tif", testing.astype(float), "Spatially held-out optical reference"),
    ):
        write_raster(output / name, values, grid, description)
    scenes = json.loads((directory / "scenes.json").read_text("utf-8"))["features"]
    sar_time = datetime.fromisoformat(scenes[0]["properties"]["datetime"].replace("Z", "+00:00"))
    optical_times = [
        datetime.fromisoformat(item["properties"]["datetime"].replace("Z", "+00:00"))
        for item in scenes[1:]
    ]
    report = {
        "status": "exploratory-optical-reference-agreement-not-ground-truth-accuracy",
        "config": config,
        "started_at": started_at,
        "environment": {
            "platform": platform.platform(),
            "python": platform.python_version(),
            "dependencies": {
                name: version(name) for name in ("numpy", "rasterio", "matplotlib", "scipy")
            },
            "gdal": rasterio.__gdal_version__,
        },
        "executed_source_sha256": {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(Path(__file__).parent.glob("*.py"))
        },
        "quality_mask_manifest_sha256": hashlib.sha256(quality_path.read_bytes()).hexdigest(),
        "quality_rules": {
            "minimum_optical_scl_class_fraction": 0.99,
            "minimum_worldcover_water_fraction": 0.999999,
            "domain": "Largest eight-connected native-water-pure component before coastal erosion",
        },
        "input_manifest_sha256": hashlib.sha256(
            (directory / "manifest.json").read_bytes()
        ).hexdigest(),
        "sar_product": config["sar"]["id"],
        "sar_acquired_at": sar_time.isoformat(),
        "optical_time_difference_hours": [
            (value - sar_time).total_seconds() / 3600 for value in optical_times
        ],
        "grid": {"crs": grid.crs, "shape": list(shape), "pixel_km2": pixel_km2},
        "counts": {
            "roi": int(roi.sum()),
            "buffered_water": int(water.sum()),
            "valid_sar_water": int(valid.sum()),
            "optical_reference": [int(np.sum(reference == c)) for c in (0, 1)],
            "training": [int(np.sum(training & (reference == c))) for c in (0, 1)],
            "heldout": [int(np.sum(testing & (reference == c))) for c in (0, 1)],
        },
        "area_km2": {
            "valid_sar_water": float(valid.sum() * pixel_km2),
            "candidate_ice": float(np.sum(prediction == 1) * pixel_km2),
            "candidate_water": float(np.sum(prediction == 0) * pixel_km2),
            "optical_reference_ice": float(np.sum(reference == 1) * pixel_km2),
            "candidate_ice_without_optical_label": float(
                np.sum((prediction == 1) & (reference < 0)) * pixel_km2
            ),
            "heldout_reference_ice": float(np.sum(testing & (reference == 1)) * pixel_km2),
            "heldout_candidate_ice": float(np.sum(testing & (prediction == 1)) * pixel_km2),
        },
        "score_sensitivity_ice_area_km2": {
            str(offset): float(
                predict_discriminant(features[valid], model, offset).sum() * pixel_km2
            )
            for offset in (-1, 0, 1)
        },
        "model": model,
        "heldout_agreement": metrics,
        "heldout_always_water_baseline": agreement_metrics(
            reference[testing], np.zeros(testing.sum())
        ),
        "heldout_blocks": block_results,
        "limitations": [
            "Optical labels are sensor-independent proxies, not field ground truth.",
            "Only bright snow-covered ice and dark water are labelled; thin/dark ice is excluded.",
            "Time mismatch permits ice drift or freeze/melt; pixel errors may be temporal.",
            "Training and test blocks share a scene and may retain spatial autocorrelation.",
            "Native class purity and coastal erosion are conservative; "
            "the largest water component is not an official marine boundary.",
            "Reflectance and SCL resolutions differ; 99% native SCL purity reduces "
            "but does not eliminate mixed-footprint uncertainty.",
            "No wind data or per-pixel incidence correction; this model is not universal.",
            "RTC calibration/terrain correction is supplied by Catalyst, not performed here.",
            "Thermal/border-noise handling and RTC processor version remain unverified.",
            "Candidate ice area is a model output, not validated total sea-ice extent.",
            "Score sensitivity is not a confidence interval.",
            "Projected UTM grid area is used, not ellipsoidal geodesic area.",
        ],
    }
    _plot_maps(output, grid, vv, vh, green, nir, swir, reference, prediction, testing, water, roi)
    replay = run_demonstration(
        directory / "scenes.json",
        output / "pipeline",
        source_uri="capture://planetary-computer/kvarken-20210330-31",
    )
    report["pipeline_run"] = {
        "scenes_ingested": replay["metrics"]["scenes_ingested"],
        "source_revision": replay["source_revision"],
        "environment_provider": replay["environment"]["provider"],
    }
    report["completed_at"] = datetime.now(UTC).isoformat()
    report["elapsed_seconds_excluding_acquisition"] = time.perf_counter() - started
    report["output_sha256"] = {
        path.relative_to(output).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(output.rglob("*"))
        if path.is_file()
    }
    _save_json(output / "results.json", report)
    return report


def _plot_maps(output, grid, vv, vh, green, nir, swir, reference, prediction, testing, water, roi):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    from matplotlib.patches import Patch

    def save_figure(figure, name):
        figure.get_layout_engine().set(rect=(0, 0.04, 1, 0.96))
        figure.text(
            0.5,
            0.008,
            "Contains modified Copernicus Sentinel data 2021",
            ha="center",
            fontsize=8,
        )
        figure.savefig(output / name, dpi=180)

    extent = (
        grid.transform.c / 1000,
        (grid.transform.c + grid.width * grid.transform.a) / 1000,
        (grid.transform.f + grid.height * grid.transform.e) / 1000,
        grid.transform.f / 1000,
    )

    def decorate(axis, title):
        axis.set(title=title, xlabel="UTM easting (km)", ylabel="UTM northing (km)")
        axis.set_aspect("equal")
        axis.annotate(
            "N",
            xy=(0.95, 0.94),
            xytext=(0.95, 0.84),
            xycoords="axes fraction",
            ha="center",
            color="white",
            bbox={"facecolor": "black", "alpha": 0.7, "pad": 2},
            arrowprops={"facecolor": "white", "edgecolor": "black", "width": 1},
        )

    fig, axes = plt.subplots(1, 2, figsize=(10, 7), constrained_layout=True)
    for axis, values, pol in zip(axes, (vv, vh), ("VV", "VH"), strict=True):
        image = axis.imshow(
            np.where(roi, values, np.nan),
            extent=extent,
            origin="upper",
            vmin=-35,
            vmax=0,
            cmap="gray",
        )
        decorate(axis, f"Sentinel-1 RTC {pol}, 30 March 2021")
        fig.colorbar(image, ax=axis, label="Gamma0 backscatter (dB)", shrink=0.7)
    fig.suptitle(
        "Kvarken | EPSG:32634 | 100 m analysis grid\nESA / Catalyst / Microsoft Planetary Computer"
    )
    save_figure(fig, "sar_input.png")
    plt.close(fig)
    fig, axis = plt.subplots(figsize=(7, 7), constrained_layout=True)
    image = axis.imshow(
        np.where(roi, vv, np.nan), extent=extent, origin="upper", vmin=-35, vmax=0, cmap="gray"
    )
    decorate(axis, "Sentinel-1 RTC VV, 30 March 2021")
    fig.colorbar(image, ax=axis, label="Gamma0 backscatter (dB)", shrink=0.7)
    fig.suptitle("Eastern Kvarken | EPSG:32634 | 100 m\nESA / Catalyst / Planetary Computer")
    save_figure(fig, "sar_vv.png")
    plt.close(fig)
    false_colour = np.stack([nir, green, swir], axis=-1)
    false_colour = np.clip(false_colour / 0.6, 0, 1)
    false_colour[~np.all(np.isfinite(false_colour), axis=-1)] = 0.7
    false_colour[~roi] = 1
    fig, axis = plt.subplots(figsize=(7, 7), constrained_layout=True)
    axis.imshow(false_colour, extent=extent, origin="upper")
    axis.legend(
        handles=[Patch(color="0.7", label="Missing optical observation")],
        loc="lower right",
        fontsize=7,
    )
    decorate(
        axis,
        "Sentinel-2, 31 March 2021: NIR / green / SWIR\nFalse colour; reflectance display 0-0.6",
    )
    fig.suptitle(
        "Independent optical sensor, not field truth | EPSG:32634\n"
        "ESA / Esri / Microsoft Planetary Computer"
    )
    save_figure(fig, "optical_input.png")
    plt.close(fig)
    fig, axes = plt.subplots(1, 3, figsize=(14, 7), constrained_layout=True)
    categorical = ListedColormap(["#2066ac", "#a6e8ed"])
    agree = np.where(testing, prediction == reference, np.nan)
    panels = (
        (
            axes[0],
            np.where(reference >= 0, reference, np.nan),
            "Conservative optical reference",
            categorical,
        ),
        (axes[1], prediction, "SAR candidate classes (not validated extent)", categorical),
        (
            axes[2],
            agree,
            "Spatially held-out agreement only",
            ListedColormap(["#d6604d", "#1b7837"]),
        ),
    )

    def draw_panel(axis, values, title, cmap):
        axis.imshow(
            np.where(water, 1, np.nan), extent=extent, origin="upper", cmap="Greys", vmin=0, vmax=2
        )
        axis.imshow(values, extent=extent, origin="upper", cmap=cmap, vmin=0, vmax=1)
        decorate(axis, title)

    for axis, values, title, cmap in panels:
        draw_panel(axis, values, title, cmap)
    class_legend = [
        Patch(color="#2066ac", label="Water"),
        Patch(color="#a6e8ed", label="Snow ice"),
        Patch(color="#808080", label="Water without label"),
        Patch(color="white", label="Excluded"),
    ]
    agreement_legend = [
        Patch(color="#1b7837", label="Agreement"),
        Patch(color="#d6604d", label="Disagreement"),
    ]
    axes[0].legend(
        handles=class_legend,
        fontsize=7,
        loc="lower right",
    )
    axes[2].legend(
        handles=agreement_legend,
        fontsize=7,
        loc="lower right",
    )
    fig.suptitle(
        "Eastern Kvarken | EPSG:32634 | 100 m grid | SAR 30 March / optical 31 March 2021\n"
        "ESA / Catalyst / Microsoft Planetary Computer; WorldCover 2021 land mask"
    )
    save_figure(fig, "classification_validation.png")
    plt.close(fig)
    for index, (_, values, title, cmap) in enumerate(panels):
        fig, axis = plt.subplots(figsize=(7, 7), constrained_layout=True)
        draw_panel(axis, values, title, cmap)
        axis.legend(
            handles=agreement_legend if index == 2 else class_legend,
            fontsize=8,
            loc="lower right",
        )
        fig.suptitle(
            "Eastern Kvarken | EPSG:32634 | 100 m\n"
            "SAR 30 / optical 31 March 2021; ESA / Catalyst / Planetary Computer\n"
            "WorldCover 2021 water domain"
        )
        save_figure(fig, ("reference.png", "candidate.png", "agreement.png")[index])
        plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--inputs-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--reuse-inputs", action="store_true")
    parser.add_argument("--resume-acquisition", action="store_true")
    parser.add_argument(
        "--prepare-quality-masks",
        action="store_true",
        help="Fetch native categorical coverage; adds an immutable supplemental manifest",
    )
    args = parser.parse_args()
    if not args.reuse_inputs:
        if args.config is None:
            parser.error("--config is required for acquisition")
        acquire(args.config, args.inputs_dir, resume=args.resume_acquisition)
    if args.prepare_quality_masks or not args.reuse_inputs:
        prepare_quality_masks(args.inputs_dir)
    result = analyze(args.inputs_dir, args.output_dir)
    print(
        json.dumps({"status": result["status"], "heldout_agreement": result["heldout_agreement"]})
    )


if __name__ == "__main__":
    main()
