"""Canonical comparability predicate (are_comparable) — CRO conditions.

Every applicable condition must pass or the pair is NOT comparable and no
YoY signal may exist. Fail closed; no warn-and-continue; no silent
normalization.
"""

from __future__ import annotations

from datetime import UTC, datetime

from _helpers import kwargs

from ares.models import InstitutionalFact, KnowledgeClass
from ares.models.ifact import are_comparable, canonical_value
from ares.models.vocab import (
    AssertionType,
    Basis,
    RevisionType,
    SubjectScopeType,
)
from ares.pipeline.entity import Entity
from ares.pipeline.facts import METRIC_REVENUE_FY_PRIOR
from ares.pipeline.signals import revenue_growth_signal
from ares.providers.edgar import _to_pipeline_facts

T1 = datetime(2026, 3, 1, tzinfo=UTC)
T2 = datetime(2026, 7, 1, tzinfo=UTC)  # decision time
T3 = datetime(2026, 8, 1, tzinfo=UTC)

FY2026 = {
    "effective_start": datetime(2025, 1, 27, tzinfo=UTC),
    "effective_end": datetime(2026, 1, 25, tzinfo=UTC),
}
FY2025 = {
    "effective_start": datetime(2024, 1, 29, tzinfo=UTC),
    "effective_end": datetime(2025, 1, 26, tzinfo=UTC),
}
FY2024 = {
    "effective_start": datetime(2023, 1, 30, tzinfo=UTC),
    "effective_end": datetime(2024, 1, 28, tzinfo=UTC),
}


def _fy(period: dict[str, datetime], **overrides: object) -> InstitutionalFact:
    return InstitutionalFact(**kwargs(retrieved_at=T1, **period, **overrides))


def test_comparable_consecutive_fy_pair_passes():
    assert are_comparable(_fy(FY2026, value=215_938_000_000), _fy(FY2025)) is True


def test_non_consecutive_fy_pair_fails():
    assert are_comparable(_fy(FY2026), _fy(FY2024)) is False


def test_different_entity_fails():
    assert are_comparable(_fy(FY2026), _fy(FY2025, subject_entity_id="AMD")) is False


def test_consolidated_vs_segment_scope_fails():
    segment = _fy(
        FY2025,
        subject_scope_type=SubjectScopeType.SEGMENT,
        subject_scope_id="CIK0001045810/datacenter",
    )
    assert are_comparable(_fy(FY2026), segment) is False


def test_different_subject_scope_id_fails():
    assert are_comparable(_fy(FY2026), _fy(FY2025, subject_scope_id="CIK0000000001")) is False


def test_different_basis_fails():
    assert are_comparable(_fy(FY2026), _fy(FY2025, basis=Basis.ADJUSTED)) is False


def test_different_unit_fails():
    assert are_comparable(_fy(FY2026), _fy(FY2025, unit="EUR", currency="USD")) is False


def test_different_currency_fails():
    assert are_comparable(_fy(FY2026), _fy(FY2025, currency="EUR")) is False


def test_different_scale_without_normalization_fails():
    assert are_comparable(_fy(FY2026), _fy(FY2025, value=130_497, scale=6)) is False


def test_explicitly_normalized_equivalent_scales_pass():
    current = _fy(FY2026, value=215_938_000_000, scale=0)
    prior_in_millions = _fy(FY2025, value=130_497, scale=6)
    assert are_comparable(current, prior_in_millions, canonical_scale=0) is True
    assert canonical_value(prior_in_millions) == 130_497_000_000.0


def test_fact_retrieved_after_decision_time_fails():
    late = InstitutionalFact(**kwargs(retrieved_at=T3, **FY2025))
    assert are_comparable(_fy(FY2026), late, decision_time=T2) is False


def test_later_restatement_is_not_used_at_earlier_decision_time():
    original = _fy(FY2026, value=215_938_000_000)
    restated = InstitutionalFact(
        **kwargs(
            retrieved_at=T3,  # restatement arrives AFTER decision time
            value=216_000_000_000,
            revision_type=RevisionType.RESTATEMENT,
            supersedes_fact_id=original.fact_id,
            **FY2026,
        )
    )
    prior = _fy(FY2025)
    assert are_comparable(restated, prior, decision_time=T2) is False  # not usable at T2
    assert are_comparable(original, prior, decision_time=T2) is True  # historical view intact


def test_unusable_fact_fails_closed():
    forecast = _fy(
        FY2025,
        assertion_type=AssertionType.FORECAST,
        knowledge_class=KnowledgeClass.HIGH_CONFIDENCE,
    )
    assert are_comparable(_fy(FY2026), forecast) is False


def _signal_from(ifacts: list[InstitutionalFact]):
    entity = Entity(entity_id="NVDA", ticker="NVDA", name="NVIDIA CORP")
    return revenue_growth_signal(entity, _to_pipeline_facts(entity, ifacts))


def test_comparable_pair_produces_signal_end_to_end():
    signal = _signal_from([_fy(FY2026, value=215_938_000_000), _fy(FY2025)])
    assert signal is not None
    assert signal.lookback_window == "FY"


def test_non_comparable_pair_produces_no_signal_end_to_end():
    # Same numbers, but the prior year is on an ADJUSTED basis: no pair, no signal.
    ifacts = [_fy(FY2026, value=215_938_000_000), _fy(FY2025, basis=Basis.ADJUSTED)]
    pipeline_facts = _to_pipeline_facts(
        Entity(entity_id="NVDA", ticker="NVDA", name="NVIDIA CORP"), ifacts
    )
    assert all(f.metric_name != METRIC_REVENUE_FY_PRIOR for f in pipeline_facts)
    assert _signal_from(ifacts) is None
