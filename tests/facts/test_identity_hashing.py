"""Deterministic identity: fact_key, content_hash, canonicalization."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from _helpers import kwargs, make_basis

from ares.models import InstitutionalFact
from ares.models.ifact import compute_content_hash
from ares.models.vocab import (
    AccountingStandard,
    AdjustmentType,
    ConsolidationScope,
    PeriodBasis,
    RevisionType,
)


def test_content_hash_is_reproducible():
    a = InstitutionalFact(**kwargs())
    b = InstitutionalFact(**kwargs())  # new fact_id, new record_created_at
    assert a.fact_id != b.fact_id
    assert a.content_hash == b.content_hash


def test_content_hash_excludes_record_time_metadata():
    a = InstitutionalFact(**kwargs(retrieved_at=datetime(2026, 8, 1, tzinfo=UTC)))
    b = InstitutionalFact(
        **kwargs(
            retrieved_at=datetime(2026, 8, 2, tzinfo=UTC),
            published_at=datetime(2025, 3, 1, tzinfo=UTC),
        )
    )
    assert a.content_hash == b.content_hash


def test_content_hash_excludes_execution_metadata():
    a = InstitutionalFact(**kwargs())
    b = InstitutionalFact(**kwargs(ingested_by="other", extractor_version="EDGAR-9.9"))
    assert a.content_hash == b.content_hash


def test_content_hash_changes_with_value():
    a = InstitutionalFact(**kwargs())
    b = InstitutionalFact(**kwargs(value=1))
    assert a.content_hash != b.content_hash


def test_canonicalization_is_order_independent():
    data = kwargs()
    reordered = dict(reversed(list(data.items())))
    assert compute_content_hash(data) == compute_content_hash(reordered)


def test_hash_survives_serialization_roundtrip():
    a = InstitutionalFact(**kwargs())
    b = InstitutionalFact.model_validate_json(a.model_dump_json())
    assert b == a
    assert b.content_hash == a.content_hash


def test_fact_key_stable_across_source_and_restatement_changes():
    original = InstitutionalFact(**kwargs())
    other_source = InstitutionalFact(
        **kwargs(source_locator="edgar:cik=1045810;accn=B2;form=10-K/A;filed=2025-06-01")
    )
    restated = InstitutionalFact(
        **kwargs(
            value=131_000_000_000,
            revision_type=RevisionType.RESTATEMENT,
            supersedes_fact_id=original.fact_id,
        )
    )
    assert original.fact_key == other_source.fact_key == restated.fact_key


def test_fact_key_changes_with_period_and_metric():
    a = InstitutionalFact(**kwargs())
    b = InstitutionalFact(
        **kwargs(
            effective_start=datetime(2023, 1, 30, tzinfo=UTC),
            effective_end=datetime(2024, 1, 28, tzinfo=UTC),
        )
    )
    c = InstitutionalFact(**kwargs(metric_ref="financial.net_income"))
    assert len({a.fact_key, b.fact_key, c.fact_key}) == 3


@pytest.mark.parametrize(
    "field_override",
    [
        {"accounting_standard": AccountingStandard.IFRS},
        {"consolidation_scope": ConsolidationScope.SEGMENT},
        {"adjustment_type": AdjustmentType.RESTATED},
        {"period_basis": PeriodBasis.TTM},
    ],
    ids=["accounting_standard", "consolidation_scope", "adjustment_type", "period_basis"],
)
def test_changing_any_basis_field_changes_fact_key(field_override):
    baseline = InstitutionalFact(**kwargs())
    changed = InstitutionalFact(**kwargs(basis=make_basis(**field_override)))
    assert changed.fact_key != baseline.fact_key
    assert changed.content_hash != baseline.content_hash


def test_basis_field_ordering_does_not_change_hash():
    data_a = kwargs()
    data_b = kwargs()
    data_b["basis"] = dict(reversed(list(dict(data_a["basis"]).items())))
    assert compute_content_hash(data_a) == compute_content_hash(data_b)


def test_all_four_basis_dimensions_appear_in_fact_key():
    key = InstitutionalFact(**kwargs()).fact_key
    assert "gaap/consolidated/as_reported/fiscal" in key


def test_fact_key_excludes_source_value_revision_retrieval():
    key = InstitutionalFact(**kwargs()).fact_key
    for token in ("edgar", "accn", "130", "api", "original"):
        assert token not in key.split("|")[0] or token == "company"
    assert "accn" not in key and "10-k" not in key and "130497000000" not in key
