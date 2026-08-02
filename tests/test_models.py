"""Smoke tests + governance checks for the ARES core models.

Runs with plain `python tests/test_models.py` (no pytest needed) or `pytest`.
It rebuilds the validated CRWV run (ARES-R-CRWV-20260801) with the models and
proves the Constitution is enforced in code.
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone

sys.path.insert(0, __file__.rsplit("/tests/", 1)[0])

from ares.models import (  # noqa: E402
    AresValidationError,
    Claim,
    Decision,
    Evidence,
    Event,
    EventType,
    Fact,
    InvestmentDecisionType,
    KnowledgeClass,
    RiskVerdict,
    Thesis,
    TimeHorizon,
)


def _utc(y, m, d):
    return datetime(y, m, d, tzinfo=timezone.utc)


def test_fact_and_calculation_gate():
    rev = Fact(
        entity_id="CRWV",
        metric_name="revenue_q1_2026",
        value=2_080_000_000,
        unit="USD",
        source_name="CoreWeave IR / CNBC",
        source_id_or_url="https://www.cnbc.com/2026/05/07/coreweave-crwv-q1-earnings-report-2026.html",
        as_of_timestamp=_utc(2026, 5, 7),
        knowledge_class=KnowledgeClass.VERIFIED_FACT,
    )
    assert rev.usable_for_calculation is True

    guess = Fact(
        entity_id="CRWV", metric_name="cash_runway_months", value=18,
        source_name="", source_id_or_url="", as_of_timestamp=_utc(2026, 5, 7),
        knowledge_class=KnowledgeClass.SPECULATION,
    )
    assert guess.usable_for_calculation is False


def test_verified_fact_requires_source():
    try:
        Fact(
            entity_id="CRWV", metric_name="x", value=1,
            source_name="", source_id_or_url="",
            as_of_timestamp=_utc(2026, 5, 7),
            knowledge_class=KnowledgeClass.VERIFIED_FACT,
        )
    except AresValidationError:
        return
    raise AssertionError("Verified Fact without a source should be rejected")


def test_catalyst_and_evidence():
    earnings = Event(
        entity_id="CRWV", event_type=EventType.EARNINGS,
        title="Q2 2026 earnings", occurs_at=_utc(2026, 8, 11),
        is_catalyst=True, expected_effect="high-impact print vs. light Q2 guide",
    )
    assert earnings.is_catalyst and earnings.is_future

    claim = Claim(
        statement="Revenue more than doubled YoY in Q1 2026",
        knowledge_class=KnowledgeClass.VERIFIED_FACT,
        supporting_fact_ids=["fact_demo"],
    )
    ev = Evidence(subject="CRWV growth", claims=[claim])
    assert ev.overall_class == KnowledgeClass.VERIFIED_FACT


def test_claim_without_support_rejected():
    try:
        Claim(statement="It will 10x", knowledge_class=KnowledgeClass.VERIFIED_FACT)
    except AresValidationError:
        return
    raise AssertionError("Verified claim without support should be rejected")


def test_crwv_thesis_builds():
    t = Thesis(
        entity_id="CRWV",
        thesis_summary=(
            "Real hypergrowth AI-infra leader with a ~$99B backlog, but a "
            "richly-priced, heavily-levered equity the whole market watches."
        ),
        hypothesis="The market underprices CRWV's solvency/refinancing risk relative to its backlog.",
        bull_case="+112% YoY revenue; ~$99B backlog; Nvidia-backed; 1->8 GW.",
        base_case="Growth continues; equity range-bound on financing overhang.",
        bear_case=(
            "~$25B debt + $740M quarterly loss = solvency/refinancing risk; "
            "15% dilution; light Q2 guide; one AI-capex pause breaks the equity."
        ),
        invalidation_conditions="Refinancing failure / major customer loss / AI-capex slowdown.",
        time_horizon=TimeHorizon.THREE_MONTHS,
        confidence=25,
        position_size=0.0,  # watchlist
    )
    assert t.confidence == 25 and t.position_size == 0.0


def test_thesis_without_bear_case_rejected():
    try:
        Thesis(
            entity_id="CRWV", thesis_summary="Looks great",
            bear_case="", invalidation_conditions="drops 20%",
        )
    except AresValidationError:
        return
    raise AssertionError("Thesis without a bear case should be rejected")


def test_human_gate_on_approve():
    # AI cannot approve: human_approved defaults False.
    try:
        Decision(
            thesis_id="thesis_demo", decision=InvestmentDecisionType.APPROVE,
            rationale="model likes it", risk_result=RiskVerdict.PASS,
        )
    except AresValidationError:
        pass
    else:
        raise AssertionError("APPROVE without human_approved should be rejected")

    # Cannot approve over a failed risk rule.
    try:
        Decision(
            thesis_id="thesis_demo", decision=InvestmentDecisionType.APPROVE,
            rationale="override", human_approved=True, risk_result=RiskVerdict.FAIL,
        )
    except AresValidationError:
        pass
    else:
        raise AssertionError("APPROVE over FAILED risk should be rejected")

    # A proper human-approved decision works.
    ok = Decision(
        thesis_id="thesis_demo", decision=InvestmentDecisionType.WATCHLIST,
        rationale="No edge; watchlist per CRWV run.",
    )
    assert ok.decision == InvestmentDecisionType.WATCHLIST


def run_all():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"  ok  {t.__name__}")
    print(f"\n{len(tests)} tests passed.")


if __name__ == "__main__":
    run_all()
