"""Tests for ARES core models (Pydantic v2): construction, governance
validators, invalid-input rejection, and serialization round-trips.

Run: pytest -q   (requires pydantic>=2.7, pytest>=8)
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from ares.models import (
    Claim,
    Decision,
    Event,
    EventType,
    Evidence,
    Fact,
    InvestmentDecisionType,
    KnowledgeClass,
    RiskResult,
    RiskVerdict,
    Scores,
    Signal,
    Thesis,
    TimeHorizon,
)


def _utc(y, m, d):
    return datetime(y, m, d, tzinfo=UTC)


def _fact():
    return Fact(
        entity_id="CRWV",
        metric_name="revenue_q1_2026",
        value=2_080_000_000,
        unit="USD",
        source_name="CoreWeave IR / CNBC",
        source_id_or_url="https://www.cnbc.com/2026/05/07/coreweave-crwv-q1-earnings-report-2026.html",
        as_of_timestamp=_utc(2026, 5, 7),
        knowledge_class=KnowledgeClass.VERIFIED_FACT,
    )


def _thesis():
    return Thesis(
        entity_id="CRWV",
        thesis_summary="Hypergrowth AI-infra leader; richly priced and heavily levered.",
        hypothesis="The market underprices CRWV solvency/refinancing risk versus its backlog.",
        bull_case="+112% YoY revenue; ~$99B backlog; Nvidia-backed.",
        base_case="Growth continues; equity range-bound on financing overhang.",
        bear_case="~$25B debt + $740M quarterly loss = solvency/refinancing risk; dilution.",
        invalidation_conditions="Refinancing failure / major customer loss / AI-capex slowdown.",
        time_horizon=TimeHorizon.THREE_MONTHS,
        scores=Scores(confidence=25, probability=40, rubric_version="RISK-1.0"),
        risk_result=RiskResult(verdict=RiskVerdict.NEEDS_REVIEW, recommended_paper_size=0.0),
    )


def test_fact_calc_gate():
    assert _fact().usable_for_calculation is True


def test_verified_fact_requires_source():
    with pytest.raises(ValidationError):
        Fact(
            entity_id="CRWV",
            metric_name="x",
            value=1,
            source_name="",
            source_id_or_url="",
            as_of_timestamp=_utc(2026, 5, 7),
            knowledge_class=KnowledgeClass.VERIFIED_FACT,
        )


def test_signal_builds_and_rejects_negative():
    s = Signal(
        entity_id="CRWV",
        signal_type="abnormal_volume",
        observed_at=_utc(2026, 8, 1),
        measured_value=3.2,
        baseline_value=1.0,
        anomaly_strength=2.2,
    )
    assert s.signal_type == "abnormal_volume"
    with pytest.raises(ValidationError):
        Signal(
            entity_id="CRWV",
            signal_type="x",
            observed_at=_utc(2026, 8, 1),
            measured_value=1.0,
            baseline_value=1.0,
            anomaly_strength=-1.0,
        )


def test_catalyst_and_evidence():
    ev = Event(
        entity_id="CRWV",
        event_type=EventType.EARNINGS,
        title="Q2 2026",
        occurs_at=_utc(2026, 8, 11),
        is_catalyst=True,
        expected_effect="high-impact print",
    )
    assert ev.is_catalyst
    e = Evidence(
        subject="CRWV growth",
        claims=[
            Claim(
                statement="Revenue doubled YoY",
                knowledge_class=KnowledgeClass.VERIFIED_FACT,
                supporting_fact_ids=["fact_x"],
            )
        ],
    )
    assert e.overall_class == KnowledgeClass.VERIFIED_FACT


def test_catalyst_without_effect_rejected():
    with pytest.raises(ValidationError):
        Event(
            entity_id="CRWV",
            event_type=EventType.EARNINGS,
            title="Q2",
            occurs_at=_utc(2026, 8, 11),
            is_catalyst=True,
        )


def test_claim_without_support_rejected():
    with pytest.raises(ValidationError):
        Claim(statement="It will 10x", knowledge_class=KnowledgeClass.VERIFIED_FACT)


def test_thesis_builds():
    t = _thesis()
    assert t.scores.confidence == 25
    assert not hasattr(t, "position_size")
    assert not hasattr(t, "confidence")


def test_thesis_requires_hypothesis():
    with pytest.raises(ValidationError):
        Thesis(
            entity_id="CRWV",
            thesis_summary="s",
            hypothesis="too short",
            bear_case="a real bear case here",
            invalidation_conditions="drops 20%",
        )


def test_thesis_without_bear_case_rejected():
    with pytest.raises(ValidationError):
        Thesis(
            entity_id="CRWV",
            thesis_summary="s",
            hypothesis="A sufficiently long testable central claim goes here.",
            bear_case="",
            invalidation_conditions="drops 20%",
        )


def test_scores_range_invalid():
    with pytest.raises(ValidationError):
        Scores(probability=150)


def test_human_gate_on_approve():
    with pytest.raises(ValidationError):
        Decision(
            thesis_id="t1",
            decision=InvestmentDecisionType.APPROVE,
            rationale="model likes it",
            risk_result=RiskResult(verdict=RiskVerdict.PASS, recommended_paper_size=2.0),
        )
    with pytest.raises(ValidationError):
        Decision(
            thesis_id="t1",
            decision=InvestmentDecisionType.APPROVE,
            rationale="override",
            human_approved=True,
            risk_result=RiskResult(verdict=RiskVerdict.FAIL, recommended_paper_size=0.0),
        )
    ok = Decision(
        thesis_id="t1", decision=InvestmentDecisionType.WATCHLIST, rationale="No edge; watchlist."
    )
    assert ok.decision == InvestmentDecisionType.WATCHLIST


def test_serialization_roundtrip():
    for obj, cls in ((_fact(), Fact), (_thesis(), Thesis)):
        d = obj.model_dump()
        assert cls.model_validate(d) == obj
        j = obj.model_dump_json()
        assert cls.model_validate_json(j) == obj
