"""Real-network EDGAR ingestion tests (opt-in: ARES_NETWORK_TESTS=1).

CI stays deterministic via the fixture tests; these prove the live path
against the actual SEC endpoints.
"""

from __future__ import annotations

import os

import pytest

from ares.pipeline import DataMode, ResearchPipeline

pytestmark = pytest.mark.skipif(
    os.environ.get("ARES_NETWORK_TESTS") != "1",
    reason="live SEC network tests are opt-in (set ARES_NETWORK_TESTS=1)",
)


def test_real_nvda_ingestion_end_to_end():
    report = ResearchPipeline(data_mode=DataMode.LIVE).run("NVDA")
    assert report.data_mode is DataMode.LIVE
    assert report.entity.name.upper().startswith("NVIDIA")
    assert len(report.facts) >= 5
    assert all(f.source_name == "SEC EDGAR" for f in report.facts)
    assert all(f.source_id_or_url.startswith("edgar:cik=") for f in report.facts)
    revenue = [f for f in report.facts if f.metric_name.startswith("revenue_fy_")]
    assert len(revenue) == 2


def test_real_unknown_ticker_fails_loudly():
    from ares.providers.edgar import EdgarError

    with pytest.raises((EdgarError, LookupError)):
        ResearchPipeline(data_mode=DataMode.LIVE).run("ZZZZZZ")
