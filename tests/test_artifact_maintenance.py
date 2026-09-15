from datetime import date

from kvarken_eo.runner import prune_live_experiment_artifacts


def test_pruning_is_dry_run_and_preserves_frozen_baseline(tmp_path):
    baseline = tmp_path / "experiment_report.json"
    baseline.write_text("baseline", encoding="utf-8")
    old_json = tmp_path / "experiment_report_live_20260101.json"
    old_md = tmp_path / "experiment_report_live_20260101.md"
    current = tmp_path / "experiment_report_live_20260915.json"
    for path in (old_json, old_md, current):
        path.write_text("artifact", encoding="utf-8")

    selected = prune_live_experiment_artifacts(tmp_path, retention_days=30, now=date(2026, 9, 15))

    assert set(selected) == {old_json, old_md}
    assert baseline.exists()
    assert old_json.exists()
    prune_live_experiment_artifacts(
        tmp_path, retention_days=30, now=date(2026, 9, 15), dry_run=False
    )
    assert not old_json.exists()
    assert not old_md.exists()
    assert current.exists()
    assert baseline.exists()
