import json
import threading
import urllib.request
from datetime import UTC, datetime

from kvarken_eo.api import create_catalog_server
from kvarken_eo.catalog import SpatialCatalog
from kvarken_eo.models import EOScene


def test_catalog_http_query_returns_filtered_json(tmp_path):
    scene = EOScene(
        "scene-api",
        "SENTINEL-2",
        datetime(2026, 9, 14, tzinfo=UTC),
        8.0,
        ((21.0, 63.0), (21.1, 63.0), (21.1, 63.1)),
        (21.0, 63.0, 21.1, 63.1),
        assets={"B04": "red.tif"},
    )
    with SpatialCatalog(tmp_path / "catalog.sqlite") as catalog:
        catalog.index_scene(scene)
        server = create_catalog_server(catalog)
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        try:
            url = f"http://127.0.0.1:{server.server_port}/api/scenes?platform=SENTINEL-2&max_cloud_cover=10"
            with urllib.request.urlopen(url) as response:
                payload = json.loads(response.read())
            assert [item["scene_id"] for item in payload["scenes"]] == ["scene-api"]
        finally:
            server.shutdown()
            thread.join()
            server.server_close()


def test_catalog_http_health_and_bad_query(tmp_path):
    with SpatialCatalog(tmp_path / "catalog.sqlite") as catalog:
        server = create_catalog_server(catalog)
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        try:
            with urllib.request.urlopen(
                f"http://127.0.0.1:{server.server_port}/api/health"
            ) as response:
                assert json.loads(response.read()) == {"status": "ok"}
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{server.server_port}/api/scenes?bbox=1,2")
            except urllib.error.HTTPError as error:
                assert error.code == 400
            else:
                raise AssertionError("invalid bbox should return HTTP 400")
        finally:
            server.shutdown()
            thread.join()
            server.server_close()
