"""Stage 5->6 (Signals) unit tests: deterministic, guarded, fact-cited."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from ares.models import Fact, KnowledgeClass
from ares.pipeline.entity import Entity, MockEntityProvider, resolve_entity
from ares.pipeline.facts import (
    METRIC_REVENUE_TTM_CURRENT,
    METRIC_REVENUE_TTM_PRIOR,
    MockFactsProvider,
    gather_facts,
)
from ares.pipeline.signals import derive_signals, revenue_growth_signal


def _nvda() -> Entity:
    return resolve_entity("NVDA", MockEntityProvider())


def _rev_fact(
    metric: str, value: float | str, knowledge_class=KnowledgeClass.HIGH_CONFIDENCE
) -> Fact:
    return Fact(
        entity_id="NVDA",
        metric_name=metric,
        value=value,
        source_name="MOCK",
        source_id_or_url="mock://x",
        as_of_timestamp=datetime(2026, 7, 31, tzinfo=UTC),
        knowledge_class=knowledge_class,
    )


def test_revenue_growth_computed_from_mock_facts():
    entity = _nvda()
    facts = gather_facts(entity, MockFactsProvider())
    signals = derive_signals(entity, facts)
    assert len(signals) == 1
    s = signals[0]
    assert s.signal_type == "revenue_growth_yoy_pct"
    # (165.2e9 - 113.3e9) / 113.3e9 * 100 = 45.81%
    assert s.measured_value == pytest.approx(45.81, abs=0.01)
    assert s.direction is not None and s.direction.value == "LONG"
    assert len(s.source_fact_ids) == 2


def test_missing_prior_year_fact_yields_no_signal():
    entity = _nvda()
    facts = [_rev_fact(METRIC_REVENUE_TTM_CURRENT, 100.0)]
    assert derive_signals(entity, facts) == []


def test_speculative_facts_are_not_usable_for_signals():
    entity = _nvda()
    facts = [
        _rev_fact(METRIC_REVENUE_TTM_CURRENT, 100.0, KnowledgeClass.SPECULATION),
        _rev_fact(METRIC_REVENUE_TTM_PRIOR, 50.0),
    ]
    assert revenue_growth_signal(entity, facts) is None


def test_zero_prior_revenue_guarded():
    entity = _nvda()
    facts = [
        _rev_fact(METRIC_REVENUE_TTM_CURRENT, 100.0),
        _rev_fact(METRIC_REVENUE_TTM_PRIOR, 0.0),
    ]
    assert revenue_growth_signal(entity, facts) is None


def test_non_numeric_values_guarded():
    entity = _nvda()
    facts = [
        _rev_fact(METRIC_REVENUE_TTM_CURRENT, "one hundred"),
        _rev_fact(METRIC_REVENUE_TTM_PRIOR, 50.0),
    ]
    assert revenue_growth_signal(entity, facts) is None


def test_foreign_facts_rejected():
    bad = _rev_fact(METRIC_REVENUE_TTM_CURRENT, 100.0)
    bad = bad.model_copy(update={"entity_id": "OTHER"})
    with pytest.raises(ValueError, match="do not belong"):
        derive_signals(_nvda(), [bad])
