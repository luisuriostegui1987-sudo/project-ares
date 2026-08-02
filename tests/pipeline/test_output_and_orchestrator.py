"""Stage 7 (Output) + orchestrator integration tests."""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from ares.models import Fact
from ares.pipeline import ResearchPipeline, render_text
from ares.pipeline.output import ResearchReport


def test_full_run_produces_valid_report():
    report = ResearchPipeline().run("NVDA")
    assert report.entity.entity_id == "NVDA"
    assert report.facts and report.evidence.claims and report.signals
    assert report.pipeline_version == "SLICE-1.0"


def test_report_serialization_roundtrip():
    report = ResearchPipeline().run("NVDA")
    restored = ResearchReport.model_validate_json(report.model_dump_json())
    assert restored == report


def test_report_rejects_claims_citing_unknown_facts():
    report = ResearchPipeline().run("NVDA")
    data = report.model_dump()
    data["facts"] = []  # drop the facts the claims cite
    with pytest.raises(ValidationError, match="cites unknown facts"):
        ResearchReport.model_validate(data)


def test_report_rejects_foreign_sections():
    report = ResearchPipeline().run("NVDA")
    data = report.model_dump()
    data["context"]["entity_id"] = "OTHER"
    with pytest.raises(ValidationError, match="foreign entity_ids"):
        ResearchReport.model_validate(data)


def test_render_text_mentions_key_sections():
    report = ResearchPipeline().run("NVDA")
    text = render_text(report)
    assert "NVIDIA" in text
    assert "revenue_growth_yoy_pct" in text
    assert "CATALYST" in text


def test_unknown_ticker_propagates_lookup_error():
    with pytest.raises(LookupError):
        ResearchPipeline().run("ZZZZ")


def test_crwv_also_runs_end_to_end():
    report = ResearchPipeline().run("crwv")
    assert report.entity.name.startswith("CoreWeave")
    assert report.signals and report.signals[0].measured_value == pytest.approx(136.84, abs=0.01)


def test_facts_in_report_are_domain_facts():
    report = ResearchPipeline().run("NVDA")
    assert all(isinstance(f, Fact) for f in report.facts)
