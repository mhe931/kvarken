"""Small standard-library HTTP query service for the scene catalog."""

import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from .catalog import SpatialCatalog
from .models import EOScene


def _scene_payload(scene: EOScene) -> dict[str, object]:
    return {
        "scene_id": scene.scene_id,
        "platform": scene.platform,
        "acquired_at": scene.acquired_at.isoformat(),
        "cloud_cover": scene.cloud_cover,
        "bbox": scene.bbox,
        "epsg": scene.epsg,
        "assets": dict(scene.assets),
    }


def create_catalog_server(
    catalog: SpatialCatalog, host: str = "127.0.0.1", port: int = 0
) -> ThreadingHTTPServer:
    class CatalogHandler(BaseHTTPRequestHandler):
        def _send(self, status: int, payload: object) -> None:
            body = json.dumps(payload, sort_keys=True).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:
            parsed = urlparse(self.path)
            if parsed.path == "/api/health":
                self._send(200, {"status": "ok"})
                return
            if parsed.path != "/api/scenes":
                self._send(404, {"error": "not found"})
                return
            try:
                query = parse_qs(parsed.query)
                bbox = _parse_bbox(query.get("bbox", [None])[0])
                max_cloud = _parse_float(query.get("max_cloud_cover", [None])[0])
                start = _parse_datetime(query.get("start", [None])[0])
                end = _parse_datetime(query.get("end", [None])[0])
                scenes = catalog.query_scenes(
                    roi=bbox,
                    platform=query.get("platform", [None])[0],
                    start_time=start,
                    end_time=end,
                    max_cloud_cover=max_cloud,
                )
            except (TypeError, ValueError) as error:
                self._send(400, {"error": str(error)})
                return
            self._send(200, {"scenes": [_scene_payload(scene) for scene in scenes]})

        def log_message(self, *_args: object) -> None:
            return

    return ThreadingHTTPServer((host, port), CatalogHandler)


def _parse_float(value: str | None) -> float | None:
    return None if value is None else float(value)


def _parse_datetime(value: str | None) -> datetime | None:
    return None if value is None else datetime.fromisoformat(value)


def _parse_bbox(value: str | None) -> tuple[float, float, float, float] | None:
    if value is None:
        return None
    parts = tuple(float(part) for part in value.split(","))
    if len(parts) != 4:
        raise ValueError("bbox must contain four comma-separated coordinates")
    return parts
