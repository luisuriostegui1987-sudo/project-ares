"""Controlled vocabularies for ARES-FACT-001 v1.0 (Sprint-2 EDGAR subset).

Every enum here is authoritative for the institutional Fact object. Values are
frozen with the spec; extending them is an ADR-level change.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class Basis(str, Enum):
    """Accounting basis of the asserted value."""

    AS_REPORTED = "AS_REPORTED"
    ADJUSTED = "ADJUSTED"
    PRO_FORMA = "PRO_FORMA"


class SubjectScopeType(str, Enum):
    """What kind of subject the fact is about."""

    COMPANY = "COMPANY"
    SEGMENT = "SEGMENT"
    INSTRUMENT = "INSTRUMENT"


class AssertionType(str, Enum):
    """Epistemic nature of the assertion."""

    REPORTED = "REPORTED"
    DERIVED = "DERIVED"
    FORECAST = "FORECAST"


class ValueType(str, Enum):
    MONEY = "MONEY"
    NUMBER = "NUMBER"
    RATIO = "RATIO"
    PER_SHARE = "PER_SHARE"
    COUNT = "COUNT"
    TEXT = "TEXT"


class PeriodType(str, Enum):
    INSTANT = "INSTANT"
    DURATION = "DURATION"


class ProvenanceType(str, Enum):
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    DERIVED = "DERIVED"
    MOCK = "MOCK"


class RetrievalMethod(str, Enum):
    API = "API"
    FILE_DOWNLOAD = "FILE_DOWNLOAD"
    MANUAL = "MANUAL"
    COMPUTED = "COMPUTED"
    MOCK = "MOCK"


class RevisionType(str, Enum):
    ORIGINAL = "ORIGINAL"
    RESTATEMENT = "RESTATEMENT"
    CORRECTION = "CORRECTION"


class ValidationStatus(str, Enum):
    """Derived from append-only FactValidationEvents — never stored on the Fact."""

    PENDING = "PENDING"
    VALID = "VALID"
    INVALID = "INVALID"
    CONFLICTED = "CONFLICTED"


class FreshnessStatus(str, Enum):
    """Derived from append-only FactFreshnessEvents — never stored on the Fact."""

    FRESH = "FRESH"
    STALE = "STALE"
    EXPIRED = "EXPIRED"


class MetricSpec(BaseModel):
    """One entry in the controlled metric registry."""

    metric_ref: str = Field(min_length=1)
    description: str = Field(min_length=1)
    value_type: ValueType
    period_type: PeriodType


# Sprint-2 controlled metric registry: only the EDGAR vertical-slice metrics.
# Mapping the full XBRL taxonomy is explicitly out of scope (ARES-FACT-001).
METRIC_REGISTRY: dict[str, MetricSpec] = {
    spec.metric_ref: spec
    for spec in (
        MetricSpec(
            metric_ref="financial.revenue",
            description="Total revenue for a fiscal period.",
            value_type=ValueType.MONEY,
            period_type=PeriodType.DURATION,
        ),
        MetricSpec(
            metric_ref="financial.net_income",
            description="Net income (loss) for a fiscal period.",
            value_type=ValueType.MONEY,
            period_type=PeriodType.DURATION,
        ),
        MetricSpec(
            metric_ref="financial.diluted_eps",
            description="Diluted earnings per share for a fiscal period.",
            value_type=ValueType.PER_SHARE,
            period_type=PeriodType.DURATION,
        ),
        MetricSpec(
            metric_ref="financial.gross_profit",
            description="Gross profit for a fiscal period.",
            value_type=ValueType.MONEY,
            period_type=PeriodType.DURATION,
        ),
        MetricSpec(
            metric_ref="financial.operating_income",
            description="Operating income (loss) for a fiscal period.",
            value_type=ValueType.MONEY,
            period_type=PeriodType.DURATION,
        ),
        MetricSpec(
            metric_ref="financial.cash_and_equivalents",
            description="Cash and cash equivalents at period end.",
            value_type=ValueType.MONEY,
            period_type=PeriodType.INSTANT,
        ),
        MetricSpec(
            metric_ref="financial.total_assets",
            description="Total assets at period end.",
            value_type=ValueType.MONEY,
            period_type=PeriodType.INSTANT,
        ),
        MetricSpec(
            metric_ref="financial.total_liabilities",
            description="Total liabilities at period end.",
            value_type=ValueType.MONEY,
            period_type=PeriodType.INSTANT,
        ),
        MetricSpec(
            metric_ref="financial.shares_outstanding",
            description="Common shares outstanding at a point in time.",
            value_type=ValueType.COUNT,
            period_type=PeriodType.INSTANT,
        ),
    )
}
