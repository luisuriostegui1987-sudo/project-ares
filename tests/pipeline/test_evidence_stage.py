"""Stage 6 (Evidence) unit tests."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from ares.models import Fact, KnowledgeClass
from ares.pipeline.entity import Entity, MockEntityProvider, resolve_entity
from ares.pipeline.evidence import derive_evidence
from ares.pipeline.facts import MockFactsProvider, gather_facts


def _nvda() -> Entity:
    return resolve_entity("NVDA", MockEntityProvider())


def _fact(entity_id: str = "NVDA", **overrides: object) -> Fact:
    base: dict[str, object] = {
        "entity_id": entity_id,
        "metric_name": "some_metric",
        "value": 42,
        "source_name": "MOCK",
        "source_id_or_url": "mock://x",
        "as_of_timestamp": datetime(2026, 7, 1, tzinfo=UTC),
        "knowledge_class": KnowledgeClass.HIGH_CONFIDENCE,
    }
    base.update(overrides)
    return Fact.model_validate(base)


def test_every_claim_cites_a_real_fact():
    entity = _nvda()
    facts = gather_facts(entity, MockFactsProvider())
    evidence = derive_evidence(entity, facts)
    known = {f.fact_id for f in facts}
    assert evidence.claims
    for claim in evidence.claims:
        assert claim.supporting_fact_ids
        assert set(claim.supporting_fact_ids) <= known


def test_knowledge_class_is_inherited_never_upgraded():
    entity = _nvda()
    facts = gather_facts(entity, MockFactsProvider())
    evidence = derive_evidence(entity, facts)
    assert all(c.knowledge_class is KnowledgeClass.HIGH_CONFIDENCE for c in evidence.claims)
    assert evidence.overall_class is KnowledgeClass.HIGH_CONFIDENCE


def test_unusable_facts_become_unresolved_questions_not_claims():
    entity = _nvda()
    facts = [
        _fact(),
        _fact(metric_name="a_rumor", knowledge_class=KnowledgeClass.SPECULATION),
    ]
    evidence = derive_evidence(entity, facts)
    assert len(evidence.claims) == 1
    assert any("a_rumor" in q for q in evidence.claims[0].unresolved_questions)


def test_foreign_facts_rejected():
    with pytest.raises(ValueError, match="do not belong"):
        derive_evidence(_nvda(), [_fact(entity_id="OTHER")])


def test_no_facts_yields_empty_evidence():
    evidence = derive_evidence(_nvda(), [])
    assert evidence.claims == []
    assert evidence.overall_class is KnowledgeClass.UNKNOWN
