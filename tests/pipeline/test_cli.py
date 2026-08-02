"""CLI tests: `ares analyze NVDA`."""
from __future__ import annotations

import json

from ares.cli import main


def test_analyze_text_output(capsys):
    assert main(["analyze", "NVDA"]) == 0
    out = capsys.readouterr().out
    assert "NVIDIA Corporation" in out
    assert "revenue_growth_yoy_pct" in out


def test_analyze_json_output(capsys):
    assert main(["analyze", "NVDA", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["entity"]["ticker"] == "NVDA"
    assert payload["pipeline_version"] == "SLICE-1.0"
    assert payload["signals"][0]["signal_type"] == "revenue_growth_yoy_pct"


def test_analyze_writes_json_file(tmp_path, capsys):
    out_file = tmp_path / "nvda.json"
    assert main(["analyze", "NVDA", "--out", str(out_file)]) == 0
    payload = json.loads(out_file.read_text())
    assert payload["entity"]["entity_id"] == "NVDA"


def test_analyze_unknown_ticker_fails_cleanly(capsys):
    assert main(["analyze", "ZZZZ"]) == 1
    assert "Unknown entity" in capsys.readouterr().err


def test_analyze_invalid_ticker_fails_cleanly(capsys):
    assert main(["analyze", "not a ticker!!"]) == 1
    assert "error:" in capsys.readouterr().err
