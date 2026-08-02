"""ARES-FACT-001 invariants: immutability, lineage, MOCK/FORECAST gates,
world-time constraints, revision sanity."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from _helpers import kwargs
from pydantic import ValidationError

from ares.facts import InMemoryFactStore
from ares.models import FactValidationEvent, InstitutionalFact, KnowledgeClass
from ares.models.vocab import (
    AssertionType,
    PeriodType,
    ProvenanceType,
    RetrievalMethod,
    RevisionType,
    ValidationStatus,
)


def test_fact_content_is_immutable():
    fact = InstitutionalFact(**kwargs())
    with pytest.raises(ValidationError):
        fact.value = 0  # type: ignore[misc]


def test_status_events_are_immutable():
    event = FactValidationEvent(
        fact_id="ifact_x", status=ValidationStatus.VALID, recorded_by="tests"
    )
    with pytest.raises(ValidationError):
        event.status = ValidationStatus.INVALID  # type: ignore[misc]


def test_store_has_no_mutation_api():
    store = InMemoryFactStore()
    for forbidden in ("update", "delete", "remove", "set_validation_status"):
        assert not hasattr(store, forbidden)


def test_derived_requires_lineage():
    with pytest.raises(ValidationError, match="lineage"):
        InstitutionalFact(
            **kwargs(
                assertion_type=AssertionType.DERIVED,
                provenance_type=ProvenanceType.DERIVED,
                retrieval_method=RetrievalMethod.COMPUTED,
                derived_from_fact_ids=[],
            )
        )


def test_primary_cannot_contain_lineage():
    with pytest.raises(ValidationError, match="PRIMARY"):
        InstitutionalFact(**kwargs(derived_from_fact_ids=["ifact_parent"]))


def test_mock_provenance_cannot_be_verified_fact():
    with pytest.raises(ValidationError, match="MOCK"):
        InstitutionalFact(**kwargs(provenance_type=ProvenanceType.MOCK))


def test_mock_retrieval_cannot_be_verified_fact():
    with pytest.raises(ValidationError, match="MOCK"):
        InstitutionalFact(**kwargs(retrieval_method=RetrievalMethod.MOCK))


def test_mock_high_confidence_is_allowed():
    fact = InstitutionalFact(
        **kwargs(
            provenance_type=ProvenanceType.MOCK,
            retrieval_method=RetrievalMethod.MOCK,
            knowledge_class=KnowledgeClass.HIGH_CONFIDENCE,
        )
    )
    assert fact.knowledge_class is KnowledgeClass.HIGH_CONFIDENCE


def test_forecast_cannot_be_verified_and_is_not_usable():
    with pytest.raises(ValidationError, match="FORECAST"):
        InstitutionalFact(**kwargs(assertion_type=AssertionType.FORECAST))
    forecast = InstitutionalFact(
        **kwargs(
            assertion_type=AssertionType.FORECAST,
            knowledge_class=KnowledgeClass.HIGH_CONFIDENCE,
        )
    )
    assert forecast.usable_for_calculation is False  # never treated as REPORTED


def test_world_time_mutual_constraints():
    with pytest.raises(ValidationError, match="INSTANT"):
        InstitutionalFact(
            **kwargs(
                period_type=PeriodType.INSTANT,
                effective_instant=None,
            )
        )
    with pytest.raises(ValidationError, match="DURATION"):
        InstitutionalFact(**kwargs(effective_end=None))
    with pytest.raises(ValidationError, match="precede"):
        InstitutionalFact(
            **kwargs(
                effective_start=datetime(2025, 1, 26, tzinfo=UTC),
                effective_end=datetime(2024, 1, 29, tzinfo=UTC),
            )
        )
    with pytest.raises(ValidationError, match="INSTANT"):
        InstitutionalFact(
            **kwargs(
                period_type=PeriodType.INSTANT,
                effective_instant=datetime(2025, 1, 26, tzinfo=UTC),
                # start/end must be absent for INSTANT
            )
        )


def test_money_requires_currency():
    with pytest.raises(ValidationError, match="currency"):
        InstitutionalFact(**kwargs(currency=None))


def test_metric_must_be_registered():
    with pytest.raises(ValidationError, match="METRIC_REGISTRY"):
        InstitutionalFact(**kwargs(metric_ref="financial.made_up_metric"))


def test_fact_cannot_supersede_itself():
    with pytest.raises(ValidationError, match="supersede itself"):
        InstitutionalFact(
            **kwargs(
                fact_id="ifact_self",
                revision_type=RevisionType.CORRECTION,
                supersedes_fact_id="ifact_self",
            )
        )


def test_original_cannot_supersede_and_revision_requires_target():
    with pytest.raises(ValidationError, match="ORIGINAL"):
        InstitutionalFact(**kwargs(supersedes_fact_id="ifact_other"))
    with pytest.raises(ValidationError, match="RESTATEMENT"):
        InstitutionalFact(**kwargs(revision_type=RevisionType.RESTATEMENT))
