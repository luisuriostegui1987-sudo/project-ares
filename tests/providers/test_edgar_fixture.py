"""Deterministic, network-free EDGAR tests against a slim companyfacts fixture."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest

from ares.models import KnowledgeClass
from ares.models.base import utcnow
from ares.models.vocab import PeriodType, ProvenanceType, ValidationStatus, ValueType
from ares.pipeline import DataMode, ResearchPipeline
from ares.pipeline.entity import Entity
from ares.pipeline.facts import (
    METRIC_REVENUE_FY_CURRENT,
    METRIC_REVENUE_FY_PRIOR,
    MockFactsProvider,
)
from ares.providers.edgar import (
    EDGAR_BASIS,
    EdgarFactsProvider,
    LiveContextProvider,
    NoEventsProvider,
    _to_pipeline_facts,
    extract_institutional_facts,
)

FIXTURE = Path(__file__).parent.parent / "fixtures" / "edgar_nvda_companyfacts_slim.json"
CIK = 1045810
RETRIEVED = datetime(2026, 8, 2, 12, 0, tzinfo=UTC)


def payload() -> dict[str, Any]:
    return json.loads(FIXTURE.read_text())


class FixtureEdgarClient:
    """Offline stand-in for EdgarClient (NOT a mock provider: fixture of real shape)."""

    def cik_for_ticker(self, ticker: str) -> int:
        return CIK

    def company_name_for_ticker(self, ticker: str) -> str:
        return "NVIDIA CORP"

    def company_facts(self, cik: int) -> dict[str, Any]:
        return payload()


def test_extracts_two_annual_revenue_facts_and_filters_quarters_and_frames():
    facts = extract_institutional_facts("NVDA", CIK, payload(), retrieved_at=RETRIEVED)
    revenue = [f for f in facts if f.metric_ref == "financial.revenue"]
    # FY2025 + FY2024; the quarterly span is excluded and the frame-annotated
    # duplicate dedupes into its fiscal period instead of double-counting.
    assert len(revenue) == 2
    values = sorted(float(f.value) for f in revenue if isinstance(f.value, (int, float)))
    assert values == [60_922_000_000.0, 130_497_000_000.0]


def test_provenance_is_exact_and_verified():
    facts = extract_institutional_facts("NVDA", CIK, payload(), retrieved_at=RETRIEVED)
    latest_revenue = max(
        (f for f in facts if f.metric_ref == "financial.revenue"),
        key=lambda f: f.effective_end or RETRIEVED,
    )
    loc = latest_revenue.source_locator
    assert "accn=0001045810-25-000023" in loc
    assert "form=10-K" in loc
    assert "filed=2025-02-26" in loc
    assert "fy=2025" in loc and "fp=FY" in loc
    assert "concept=us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax" in loc
    assert "unit=USD" in loc
    assert latest_revenue.provenance_type is ProvenanceType.PRIMARY
    assert latest_revenue.knowledge_class is KnowledgeClass.VERIFIED_FACT
    assert latest_revenue.published_at == datetime(2025, 2, 26, tzinfo=UTC)


def test_metric_registry_types_are_respected():
    facts = {f.metric_ref: f for f in extract_institutional_facts("NVDA", CIK, payload())}
    assert facts["financial.diluted_eps"].value_type is ValueType.PER_SHARE
    assert facts["financial.shares_outstanding"].value_type is ValueType.COUNT
    assert facts["financial.total_assets"].period_type is PeriodType.INSTANT
    assert facts["financial.revenue"].period_type is PeriodType.DURATION
    assert facts["financial.cash_and_equivalents"].effective_instant == datetime(
        2025, 1, 26, tzinfo=UTC
    )


def test_edgar_facts_carry_conditionally_classified_basis():
    facts = extract_institutional_facts("NVDA", CIK, payload(), retrieved_at=RETRIEVED)
    assert facts
    gaap = [f for f in facts if f.metric_ref != "financial.shares_outstanding"]
    assert gaap and all(f.basis == EDGAR_BASIS for f in gaap)
    shares = next(f for f in facts if f.metric_ref == "financial.shares_outstanding")
    # dei registrant metadata: NOT auto-labeled GAAP (approved rule => NA).
    assert shares.basis.accounting_standard.value == "NA"
    assert shares.basis.consolidation_scope.value == "CONSOLIDATED"
    assert shares.basis.adjustment_type.value == "AS_REPORTED"
    assert shares.basis.period_basis.value == "FISCAL"


def test_extraction_is_deterministic():
    a = extract_institutional_facts("NVDA", CIK, payload(), retrieved_at=RETRIEVED)
    b = extract_institutional_facts("NVDA", CIK, payload(), retrieved_at=RETRIEVED)
    assert [f.fact_key for f in a] == [f.fact_key for f in b]
    assert [f.content_hash for f in a] == [f.content_hash for f in b]


def test_retrieved_at_is_stamped_now_never_backdated():
    before = utcnow()
    facts = extract_institutional_facts("NVDA", CIK, payload())
    after = utcnow()
    assert all(before <= f.retrieved_at <= after for f in facts)


def test_pipeline_fact_adaptation_keeps_ids_and_provenance():
    entity = Entity(entity_id="NVDA", ticker="NVDA", name="NVIDIA CORP")
    ifacts = extract_institutional_facts("NVDA", CIK, payload(), retrieved_at=RETRIEVED)
    pipeline_facts = _to_pipeline_facts(entity, ifacts)
    by_name = {f.metric_name: f for f in pipeline_facts}
    current = by_name[METRIC_REVENUE_FY_CURRENT]
    prior = by_name[METRIC_REVENUE_FY_PRIOR]
    assert current.value == 130_497_000_000
    assert prior.value == 60_922_000_000
    assert current.source_name == "SEC EDGAR"
    assert "accn=0001045810-25-000023" in current.source_id_or_url
    ids = {f.fact_id for f in ifacts}
    assert current.fact_id in ids and prior.fact_id in ids  # report cites the store


def test_provider_stores_facts_and_marks_them_valid():
    provider = EdgarFactsProvider(FixtureEdgarClient())  # type: ignore[arg-type]
    entity = Entity(entity_id="NVDA", ticker="NVDA", name="NVIDIA CORP")
    provider.facts_for(entity)
    stored = provider.store.all_facts()
    assert len(stored) >= 9
    assert all(
        provider.store.validation_status(f.fact_id) is ValidationStatus.VALID for f in stored
    )
    # Re-ingestion dedupes deterministically instead of duplicating.
    provider.facts_for(entity)
    assert len(provider.store.all_facts()) == len(stored)


def _live_pipeline() -> ResearchPipeline:
    client = FixtureEdgarClient()
    return ResearchPipeline(
        entity_provider=_FixtureEntityProvider(),
        context_provider=LiveContextProvider(client),  # type: ignore[arg-type]
        events_provider=NoEventsProvider(),
        facts_provider=EdgarFactsProvider(client),  # type: ignore[arg-type]
        data_mode=DataMode.LIVE,
    )


class _FixtureEntityProvider:
    def resolve(self, ticker: str) -> Entity:
        return Entity(entity_id=ticker, ticker=ticker, name="NVIDIA CORP")


def test_live_report_end_to_end_offline():
    report = _live_pipeline().run("NVDA")
    assert report.data_mode is DataMode.LIVE
    assert report.signals, "FY revenue pair must produce the growth signal"
    signal = report.signals[0]
    assert signal.signal_type == "revenue_growth_yoy_pct"
    assert signal.lookback_window == "FY"
    assert signal.measured_value == pytest.approx(114.2, abs=0.1)  # 60.9B -> 130.5B
    assert all(f.source_name == "SEC EDGAR" for f in report.facts)


def test_live_mode_rejects_mock_providers():
    with pytest.raises(ValueError, match="mock providers"):
        ResearchPipeline(facts_provider=MockFactsProvider(), data_mode=DataMode.LIVE)


def test_live_cli_failure_is_loud_not_silent(monkeypatch, capsys):
    from ares.cli import main
    from ares.providers import edgar

    def boom(self: object, url: str) -> None:
        raise edgar.EdgarError("simulated SEC outage")

    monkeypatch.setattr(edgar.EdgarClient, "_get_json", boom)
    assert main(["analyze", "NVDA", "--data-mode", "live"]) == 1
    err = capsys.readouterr().err
    assert "live EDGAR retrieval failed" in err
    assert "never falls back to mock data" in err
