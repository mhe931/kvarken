import os
from datetime import UTC, datetime, timedelta

from kvarken_eo import EOScene, FileProvenanceSink, SpatialCatalog


def test_orphan_detection_is_dry_run_by_default(tmp_path):
    sink = FileProvenanceSink(tmp_path / "provenance")
    payload = {"scene_id": "scene-1", "value": 1}
    record = sink.store(
        source_id="scene-1",
        collection="test",
        source_uri="fixture://scene-1",
        payload=payload,
    )
    orphan = sink._raw_dir / "orphan.json"
    orphan.write_text("{}", encoding="utf-8")
    scene = EOScene(
        "scene-1",
        "test",
        datetime.now(UTC),
        0,
        ((21, 63), (21.1, 63), (21.1, 63.1)),
        (21, 63, 21.1, 63.1),
    )
    with SpatialCatalog(tmp_path / "catalog.sqlite") as catalog:
        catalog.index_scene(scene)
        candidates = sink.prune_raw_payloads(catalog)
        assert orphan in candidates
        assert (tmp_path / "provenance" / record.raw_payload_path).exists()
        sink.prune_raw_payloads(catalog, dry_run=False)
    assert not orphan.exists()


def test_old_payloads_are_selected_by_retention(tmp_path):
    sink = FileProvenanceSink(tmp_path / "provenance")
    record = sink.store(
        source_id="old",
        collection="test",
        source_uri="fixture://old",
        payload={"old": True},
        ingested_at=datetime.now(UTC) - timedelta(days=30),
    )
    old_path = tmp_path / "provenance" / record.raw_payload_path
    old_timestamp = (datetime.now(UTC) - timedelta(days=30)).timestamp()
    os.utime(old_path, (old_timestamp, old_timestamp))
    candidates = sink.find_orphaned_payloads(older_than=datetime.now(UTC) - timedelta(days=1))
    assert len(candidates) == 1
