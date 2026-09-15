import json
from datetime import UTC, datetime

import pytest

from kvarken_eo.runner import resolve_cdse_settings, run_live_experiment


def test_resolve_cdse_settings_requires_all_credentials():
    assert resolve_cdse_settings({}) is None
    values = {
        "CDSE_TOKEN_URL": "https://identity.example/token",
        "CDSE_CLIENT_ID": "client",
        "CDSE_CLIENT_SECRET": "secret",
        "CDSE_STAC_URL": "https://stac.example",
    }
    settings = resolve_cdse_settings(values)
    assert settings is not None
    assert settings.stac_url == "https://stac.example"


def test_live_runner_uses_offline_fallback_and_dated_artifact(tmp_path):
    output = run_live_experiment(
        tmp_path,
        environ={},
        now=datetime(2026, 9, 15, 9, 10, tzinfo=UTC),
        limit=1,
    )

    assert output.name == "experiment_report_live_20260915.json"
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["run"]["mode"] == "offline-fallback"
    assert report["run"]["items_returned"] == 1
    assert report["network"]["search_round_trip_ms"] >= 0
    assert (tmp_path / "experiment_report_live_20260915.md").exists()
    with pytest.raises(FileExistsError):
        run_live_experiment(
            tmp_path,
            environ={},
            now=datetime(2026, 9, 15, 12, tzinfo=UTC),
            limit=1,
        )
