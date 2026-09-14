from kvarken_eo.__main__ import main


def test_verify_health_command_returns_success(capsys):
    assert main(["verify-health"]) == 0
    assert "health check passed" in capsys.readouterr().out
