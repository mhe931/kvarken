import hashlib
import json
from pathlib import Path

import pytest

from kvarken_eo.demonstration import run_demonstration

FIXTURE = Path(__file__).parent / "fixtures" / "stac_search_page_1.json"


def test_replay_preserves_input_and_verifies_catalog_provenance_and_api(tmp_path):
    output = tmp_path / "run"
    report = run_demonstration(
        FIXTURE, output, source_uri="fixture://stac_search_page_1", concurrency=2
    )

    source = FIXTURE.read_bytes()
    assert (output / "input.json").read_bytes() == source
    assert report["input"]["sha256"] == hashlib.sha256(source).hexdigest()
    assert report["workload"] == "metadata-catalog-replay"
    assert report["environment"]["provider"] == "not-verified"
    assert report["validation"]["catalog_reopened"] is True
    assert report["validation"]["api_health"] == {"status": "ok"}
    assert report["validation"]["scene_ids"] == [
        feature["id"] for feature in json.loads(source)["features"]
    ]
    assert report["validation"]["provenance_records"] == len(json.loads(source)["features"])
    assert report["metrics"]["scenes_ingested"] == len(json.loads(source)["features"])
    assert report["metrics"]["failure_count"] == 0
    assert report["started_at"] <= report["completed_at"]
    assert report["elapsed_seconds"] > 0
    assert len(report["source_revision"]["sha"]) == 40
    assert json.loads((output / "run.json").read_text()) == report
    for relative, digest in report["output_sha256"].items():
        assert hashlib.sha256((output / relative).read_bytes()).hexdigest() == digest


def test_replay_refuses_existing_output_directory(tmp_path):
    (tmp_path / "existing").mkdir()
    with pytest.raises(FileExistsError):
        run_demonstration(FIXTURE, tmp_path / "existing", source_uri="fixture://test")


@pytest.mark.parametrize("concurrency", [0, -1])
def test_replay_rejects_invalid_worker_limit_before_creating_output(tmp_path, concurrency):
    output = tmp_path / "invalid"
    with pytest.raises(ValueError, match="concurrency"):
        run_demonstration(FIXTURE, output, source_uri="fixture://test", concurrency=concurrency)
    assert not output.exists()


@pytest.mark.parametrize("mutation", ["empty", "duplicate", "invalid", "coordinates"])
def test_replay_rejects_invalid_input_before_creating_output(tmp_path, mutation):
    payload = json.loads(FIXTURE.read_text())
    if mutation == "empty":
        payload["features"] = []
    elif mutation == "duplicate":
        payload["features"].append(payload["features"][0])
    elif mutation == "coordinates":
        payload["features"][0]["geometry"]["coordinates"][0][0][0] = 500000
    else:
        del payload["features"][0]["properties"]["datetime"]
    input_path = tmp_path / "input.json"
    input_path.write_text(json.dumps(payload))
    output = tmp_path / "invalid"
    with pytest.raises(ValueError):
        run_demonstration(input_path, output, source_uri="fixture://test")
    assert not output.exists()


def test_replay_does_not_persist_signed_or_authenticated_source_urls(tmp_path):
    with pytest.raises(ValueError, match="public"):
        run_demonstration(
            FIXTURE,
            tmp_path / "invalid",
            source_uri="https://example.org/item?access_token=do-not-store",
        )
    assert not (tmp_path / "invalid").exists()


def test_replay_preserves_each_items_original_self_uri(tmp_path):
    payload = json.loads(FIXTURE.read_text())
    payload["features"][0]["links"] = [
        {"rel": "self", "href": "https://example.org/collections/optical/items/scene"}
    ]
    input_path = tmp_path / "page.json"
    input_path.write_text(json.dumps(payload))
    run_demonstration(input_path, tmp_path / "run", source_uri="capture://real-satellite-items")
    record = json.loads((tmp_path / "run/provenance/manifest.jsonl").read_text())
    assert record["source_uri"] == "https://example.org/collections/optical/items/scene"
