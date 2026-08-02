"""Point-in-time safety and append-only revision behavior (ARES-FACT-001)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from _helpers import kwargs

from ares.facts import FactStoreError, InMemoryFactStore
from ares.models import FactFreshnessEvent, FactValidationEvent, InstitutionalFact
from ares.models.base import utcnow
from ares.models.vocab import FreshnessStatus, RevisionType, ValidationStatus

T1 = datetime(2026, 6, 1, tzinfo=UTC)
T2 = datetime(2026, 7, 1, tzinfo=UTC)  # decision time
T3 = datetime(2026, 8, 1, tzinfo=UTC)


def _store_with_restatement() -> tuple[InMemoryFactStore, InstitutionalFact, InstitutionalFact]:
    store = InMemoryFactStore()
    original = store.append(InstitutionalFact(**kwargs(retrieved_at=T1)))
    restated = store.append(
        InstitutionalFact(
            **kwargs(
                value=131_000_000_000,
                retrieved_at=T3,
                revision_type=RevisionType.RESTATEMENT,
                supersedes_fact_id=original.fact_id,
            )
        )
    )
    return store, original, restated


def test_retrieved_at_cannot_be_in_the_future():
    store = InMemoryFactStore()
    with pytest.raises(FactStoreError, match="future"):
        store.append(InstitutionalFact(**kwargs(retrieved_at=utcnow() + timedelta(days=2))))


def test_historical_query_cannot_see_later_retrievals():
    store, original, restated = _store_with_restatement()
    visible = store.facts_as_of(T2)
    assert [f.fact_id for f in visible] == [original.fact_id]
    assert restated.fact_id not in {f.fact_id for f in visible}  # no lookahead bias


def test_restatement_is_a_new_fact_and_original_remains_intact():
    store, original, restated = _store_with_restatement()
    assert restated.fact_id != original.fact_id
    assert restated.fact_key == original.fact_key  # same logical identity
    stored_original = store.get(original.fact_id)
    assert stored_original.value == 130_497_000_000  # untouched
    assert stored_original.revision_type is RevisionType.ORIGINAL
    assert len(store.by_fact_key(original.fact_key)) == 2


def test_is_current_is_derived_by_reverse_lookup_and_point_in_time():
    store, original, restated = _store_with_restatement()
    # At decision time T2 the restatement did not exist yet: original was current.
    assert store.is_current(original.fact_id, as_of=T2) is True
    # Today, the restatement supersedes it.
    assert store.is_current(original.fact_id) is False
    assert store.is_current(restated.fact_id) is True
    current_now = store.current_facts_as_of(utcnow())
    assert [f.fact_id for f in current_now] == [restated.fact_id]


def test_supersession_chains_are_acyclic():
    store, original, restated = _store_with_restatement()
    third = store.append(
        InstitutionalFact(
            **kwargs(
                value=132_000_000_000,
                retrieved_at=T3,
                revision_type=RevisionType.CORRECTION,
                supersedes_fact_id=restated.fact_id,
            )
        )
    )
    assert store.is_current(third.fact_id)
    with pytest.raises(FactStoreError, match="not in the store"):
        store.append(
            InstitutionalFact(
                **kwargs(
                    value=1,
                    retrieved_at=T3,
                    revision_type=RevisionType.CORRECTION,
                    supersedes_fact_id="ifact_ghost",
                )
            )
        )
    # Corrupt-state guard: a cycle is impossible through the public API (a new
    # fact must reference an EXISTING id), so exercise the walker directly.
    crafted = InstitutionalFact(
        **kwargs(
            value=2,
            retrieved_at=T3,
            revision_type=RevisionType.CORRECTION,
            supersedes_fact_id=original.fact_id,
        )
    )
    store._facts[original.fact_id] = original.model_copy(
        update={"supersedes_fact_id": crafted.fact_id}
    )
    with pytest.raises(FactStoreError, match="cycle"):
        store._check_chain_acyclic(crafted)


def test_multiple_sources_share_one_fact_key():
    store = InMemoryFactStore()
    a = store.append(InstitutionalFact(**kwargs(retrieved_at=T1)))
    b = store.append(
        InstitutionalFact(
            **kwargs(
                retrieved_at=T1,
                source_locator="edgar:cik=1045810;accn=OTHER;form=10-K/A;filed=2025-06-01",
            )
        )
    )
    assert a.fact_id != b.fact_id
    assert {f.fact_id for f in store.by_fact_key(a.fact_key)} == {a.fact_id, b.fact_id}


def test_deterministic_deduplication():
    store = InMemoryFactStore()
    a = store.append(InstitutionalFact(**kwargs(retrieved_at=T1)))
    duplicate = store.append(InstitutionalFact(**kwargs(retrieved_at=T1)))
    assert duplicate.fact_id == a.fact_id
    assert len(store.all_facts()) == 1


def test_status_is_derived_from_append_only_events():
    store = InMemoryFactStore()
    fact = store.append(InstitutionalFact(**kwargs(retrieved_at=T1)))
    assert store.validation_status(fact.fact_id) is ValidationStatus.PENDING
    assert store.usable_for_calculation(fact.fact_id) is False  # not yet VALID
    store.add_validation_event(
        FactValidationEvent(
            fact_id=fact.fact_id,
            status=ValidationStatus.VALID,
            recorded_by="tests",
            occurred_at=T1,
        )
    )
    assert store.validation_status(fact.fact_id) is ValidationStatus.VALID
    assert store.usable_for_calculation(fact.fact_id) is True
    store.add_validation_event(
        FactValidationEvent(
            fact_id=fact.fact_id,
            status=ValidationStatus.CONFLICTED,
            recorded_by="tests",
            occurred_at=T3,
        )
    )
    assert store.validation_status(fact.fact_id) is ValidationStatus.CONFLICTED
    assert store.usable_for_calculation(fact.fact_id) is False
    assert len(store.validation_history(fact.fact_id)) == 2  # history preserved
    assert store.freshness_status(fact.fact_id) is FreshnessStatus.FRESH
    store.add_freshness_event(
        FactFreshnessEvent(fact_id=fact.fact_id, status=FreshnessStatus.STALE, recorded_by="tests")
    )
    assert store.freshness_status(fact.fact_id) is FreshnessStatus.STALE
