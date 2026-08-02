"""Stage 4 (Facts) unit tests."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from ares.models import Fact, KnowledgeClass
from ares.pipeline.entity import Entity, MockEntityProvider, resolve_entity
from ares.pipeline.facts import (
    METRIC_GROSS_MARGIN_PCT,
    METRIC_REVENUE_TTM_CURRENT,
    MockFactsProvider,
    gather_facts,
)


def _nvda() -> Entity:
    return resolve_entity("NVDA", MockEntityProvider())


def test_facts_gathered_are_owned_sourced_and_usable():
    facts = gather_facts(_nvda(), MockFactsProvider())
    assert {f.metric_name for f in facts} >= {METRIC_REVENUE_TTM_CURRENT, METRIC_GROSS_MARGIN_PCT}
    assert all(f.entity_id == "NVDA" for f in facts)
    assert all(f.source_id_or_url.startswith("mock://") for f in facts)
    assert all(f.usable_for_calculation for f in facts)


def test_mock_facts_are_labeled_mock_not_verified():
    facts = gather_facts(_nvda(), MockFactsProvider())
    assert all(f.knowledge_class is KnowledgeClass.HIGH_CONFIDENCE for f in facts)
    assert all("MOCK" in f.source_name for f in facts)


def test_foreign_facts_rejected():
    class BadProvider:
        def facts_for(self, entity: Entity) -> list[Fact]:
            return [
                Fact(
                    entity_id="OTHER",
                    metric_name="x",
                    value=1,
                    source_name="s",
                    source_id_or_url="mock://x",
                    as_of_timestamp=datetime(2026, 7, 1, tzinfo=UTC),
                    knowledge_class=KnowledgeClass.HIGH_CONFIDENCE,
                )
            ]

    with pytest.raises(ValueError, match="do not belong"):
        gather_facts(_nvda(), BadProvider())
