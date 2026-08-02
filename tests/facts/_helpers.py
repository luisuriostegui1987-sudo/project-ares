"""Shared builder for InstitutionalFact test kwargs."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from ares.models import KnowledgeClass
from ares.models.vocab import (
    AccountingStandard,
    AdjustmentType,
    AssertionType,
    Basis,
    ConsolidationScope,
    PeriodBasis,
    PeriodType,
    ProvenanceType,
    RetrievalMethod,
    SubjectScopeType,
    ValueType,
)


def make_basis(**overrides: Any) -> Basis:
    base: dict[str, Any] = {
        "accounting_standard": AccountingStandard.GAAP,
        "consolidation_scope": ConsolidationScope.CONSOLIDATED,
        "adjustment_type": AdjustmentType.AS_REPORTED,
        "period_basis": PeriodBasis.FISCAL,
    }
    base.update(overrides)
    return Basis(**base)


def kwargs(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "subject_entity_id": "NVDA",
        "subject_scope_type": SubjectScopeType.COMPANY,
        "subject_scope_id": "CIK0001045810",
        "metric_ref": "financial.revenue",
        "basis": make_basis(),
        "assertion_type": AssertionType.REPORTED,
        "value": 130_497_000_000,
        "value_type": ValueType.MONEY,
        "unit": "USD",
        "currency": "USD",
        "period_type": PeriodType.DURATION,
        "effective_start": datetime(2024, 1, 29, tzinfo=UTC),
        "effective_end": datetime(2025, 1, 26, tzinfo=UTC),
        "published_at": datetime(2025, 2, 26, tzinfo=UTC),
        "retrieved_at": datetime(2026, 8, 1, tzinfo=UTC),
        "source_id": "sec.edgar",
        "source_locator": "edgar:cik=1045810;accn=A1;form=10-K;filed=2025-02-26",
        "provenance_type": ProvenanceType.PRIMARY,
        "retrieval_method": RetrievalMethod.API,
        "knowledge_class": KnowledgeClass.VERIFIED_FACT,
        "ingested_by": "tests",
        "extractor_version": "EDGAR-1.0",
    }
    base.update(overrides)
    return base
