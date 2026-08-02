"""Conditional, conservative Basis classification for EDGAR observations.

Every dimension must be evidenced by the observation itself; anything
ambiguous is rejected (no LIVE Fact emitted) — never mislabeled.
"""

from __future__ import annotations

from typing import Any

from ares.models.vocab import (
    AccountingStandard,
    AdjustmentType,
    ConsolidationScope,
    PeriodBasis,
    PeriodType,
)
from ares.providers.edgar import EDGAR_BASIS, classify_basis, extract_institutional_facts

CIK = 1045810


def _item(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "start": "2024-01-29",
        "end": "2025-01-26",
        "val": 130_497_000_000,
        "accn": "0001045810-25-000023",
        "fy": 2025,
        "fp": "FY",
        "form": "10-K",
        "filed": "2025-02-26",
    }
    base.update(overrides)
    return base


def test_undimensioned_original_usgaap_annual_gets_full_standard_basis():
    basis = classify_basis("us-gaap", _item(), PeriodType.DURATION)
    assert basis == EDGAR_BASIS
    assert basis is not None
    assert basis.accounting_standard is AccountingStandard.GAAP
    assert basis.consolidation_scope is ConsolidationScope.CONSOLIDATED
    assert basis.adjustment_type is AdjustmentType.AS_REPORTED
    assert basis.period_basis is PeriodBasis.FISCAL


def test_dimensional_segment_context_is_never_consolidated():
    basis = classify_basis(
        "us-gaap",
        _item(segment={"us-gaap:StatementBusinessSegmentsAxis": "DataCenter"}),
        PeriodType.DURATION,
    )
    assert basis is None  # rejected: never labeled CONSOLIDATED


def test_amended_filing_is_not_as_reported():
    basis = classify_basis("us-gaap", _item(form="10-K/A"), PeriodType.DURATION)
    assert basis is not None
    assert basis.adjustment_type is AdjustmentType.RESTATED
    quarterly = classify_basis("us-gaap", _item(form="10-Q/A", fp="Q3"), PeriodType.DURATION)
    assert quarterly is not None
    assert quarterly.adjustment_type is AdjustmentType.RESTATED


def test_issuer_extension_concept_is_not_automatically_gaap():
    assert classify_basis("nvda", _item(), PeriodType.DURATION) is None


def test_dei_is_registrant_metadata_not_gaap():
    basis = classify_basis("dei", _item(), PeriodType.INSTANT)
    assert basis is not None
    assert basis.accounting_standard is AccountingStandard.NA


def test_ttm_marker_classifies_ttm_not_fiscal():
    basis = classify_basis("us-gaap", _item(fp="TTM"), PeriodType.DURATION)
    assert basis is not None
    assert basis.period_basis is PeriodBasis.TTM


def test_ambiguous_dimensions_reject_the_observation():
    assert classify_basis("us-gaap", _item(form=None), PeriodType.DURATION) is None
    assert classify_basis("us-gaap", _item(fp=None), PeriodType.DURATION) is None
    assert classify_basis("us-gaap", _item(fy=None), PeriodType.DURATION) is None


def test_unsafe_observation_emits_no_live_fact():
    """An instant item with no fiscal metadata must be dropped by extraction."""
    payload = {
        "cik": CIK,
        "entityName": "NVIDIA CORP",
        "facts": {
            "us-gaap": {
                "Assets": {
                    "units": {
                        "USD": [
                            {
                                "end": "2026-01-25",
                                "val": 259_474_000_000,
                                "accn": "0001045810-26-000021",
                                "form": "10-K",
                                "filed": "2026-02-25",
                            }  # no fy/fp: ambiguous
                        ]
                    }
                }
            }
        },
    }
    facts = extract_institutional_facts("NVDA", CIK, payload)
    assert facts == []
