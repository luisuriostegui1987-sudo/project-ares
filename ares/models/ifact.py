"""InstitutionalFact — ARES-FACT-001 v1.0 (Sprint-2 EDGAR subset).

The institutional Fact object: immutable, append-only, deterministically
identified. Content never mutates; corrections and restatements are NEW facts
linked through supersedes_fact_id. Validation and freshness are NOT stored on
the fact — they are derived from append-only status events.

Identity model:
- fact_key      logical identity (subject + scope + metric + basis + world-time
                period). Excludes source, value, revision, retrieval metadata —
                so multiple sources / restatements share one fact_key.
- fact_id       unique immutable record identity.
- content_hash  SHA-256 over canonical assertion content. Excludes
                published_at / retrieved_at / record_created_at, status events
                and execution metadata — reproducible by construction.
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, model_validator

from .base import new_id, utcnow
from .enums import KnowledgeClass
from .vocab import (
    METRIC_REGISTRY,
    AssertionType,
    Basis,
    FreshnessStatus,
    PeriodType,
    ProvenanceType,
    RetrievalMethod,
    RevisionType,
    SubjectScopeType,
    ValidationStatus,
    ValueType,
)

SCHEMA_VERSION = "ARES-FACT-001/1.0"


def _iso(dt: datetime | None) -> str | None:
    return dt.astimezone(UTC).isoformat() if dt is not None else None


def compute_fact_key(
    subject_scope_type: SubjectScopeType,
    subject_scope_id: str,
    metric_ref: str,
    basis: Basis,
    period_type: PeriodType,
    effective_instant: datetime | None,
    effective_start: datetime | None,
    effective_end: datetime | None,
) -> str:
    """Deterministic logical identity. No source, value, revision or retrieval data."""
    if period_type is PeriodType.INSTANT:
        period = _iso(effective_instant) or ""
    else:
        period = f"{_iso(effective_start) or ''}..{_iso(effective_end) or ''}"
    return (
        f"{subject_scope_type.value}:{subject_scope_id}"
        f"|{metric_ref}|{basis.value}|{period_type.value}:{period}"
    ).lower()


# Fields hashed into content_hash. Deliberately excludes: fact_id (record id),
# published_at / retrieved_at / record_created_at (timestamps), status events
# (separate objects) and execution metadata (ingested_by, extractor_version,
# model_id, prompt_version).
_HASHED_FIELDS = (
    "schema_version",
    "fact_key",
    "subject_entity_id",
    "subject_scope_type",
    "subject_scope_id",
    "metric_ref",
    "basis",
    "assertion_type",
    "value",
    "value_type",
    "unit",
    "currency",
    "scale",
    "precision",
    "uncertainty",
    "effective_instant",
    "effective_start",
    "effective_end",
    "period_type",
    "source_id",
    "source_locator",
    "provenance_type",
    "retrieval_method",
    "derived_from_fact_ids",
    "corroborating_fact_ids",
    "knowledge_class",
    "revision_type",
    "supersedes_fact_id",
)


def compute_content_hash(data: dict[str, Any]) -> str:
    """SHA-256 over the canonical JSON form of the assertion content."""
    payload: dict[str, Any] = {}
    for name in _HASHED_FIELDS:
        v = data.get(name)
        if isinstance(v, datetime):
            v = _iso(v)
        elif isinstance(v, Enum):
            v = v.value
        elif isinstance(v, list):
            v = sorted(str(i) for i in v)
        payload[name] = v
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class InstitutionalFact(BaseModel):
    """One immutable, sourced, deterministically-identified assertion."""

    model_config = {"frozen": True}

    # Identity
    fact_id: str = Field(default_factory=lambda: new_id("ifact"))
    fact_key: str = ""  # filled deterministically if omitted; always verified
    schema_version: str = SCHEMA_VERSION

    # Subject
    subject_entity_id: str = Field(min_length=1)
    subject_scope_type: SubjectScopeType
    subject_scope_id: str = Field(min_length=1)

    # Assertion
    metric_ref: str = Field(min_length=1)
    basis: Basis
    assertion_type: AssertionType
    value: float | int | str
    value_type: ValueType
    unit: str | None = None
    currency: str | None = None
    scale: int = 0
    precision: int | None = None
    uncertainty: float | None = Field(default=None, ge=0)

    # World time
    effective_instant: datetime | None = None
    effective_start: datetime | None = None
    effective_end: datetime | None = None
    period_type: PeriodType

    # Record time
    published_at: datetime
    retrieved_at: datetime
    valid_until: datetime | None = None

    # Provenance
    source_id: str = Field(min_length=1)
    source_locator: str = Field(min_length=1)
    provenance_type: ProvenanceType
    retrieval_method: RetrievalMethod
    derived_from_fact_ids: list[str] = Field(default_factory=list)
    knowledge_class: KnowledgeClass
    corroborating_fact_ids: list[str] = Field(default_factory=list)

    # Revision (append-only: revisions are NEW facts)
    revision_type: RevisionType = RevisionType.ORIGINAL
    supersedes_fact_id: str | None = None

    # Integrity & execution metadata
    content_hash: str = ""  # filled deterministically if omitted; always verified
    ingested_by: str = Field(min_length=1)
    extractor_version: str = Field(min_length=1)
    model_id: str | None = None
    prompt_version: str | None = None
    record_created_at: datetime = Field(default_factory=utcnow)

    @model_validator(mode="before")
    @classmethod
    def _fill_identity(cls, data: Any) -> Any:
        if isinstance(data, dict):
            try:
                return cls._fill_identity_inner(data)
            except (KeyError, ValueError):
                # Missing/invalid required fields: let field validation report them.
                return data
        return data

    @classmethod
    def _fill_identity_inner(cls, data: dict[str, Any]) -> dict[str, Any]:
        if not data.get("fact_key"):
            data["fact_key"] = compute_fact_key(
                SubjectScopeType(data["subject_scope_type"]),
                data["subject_scope_id"],
                data["metric_ref"],
                Basis(data["basis"]),
                PeriodType(data["period_type"]),
                data.get("effective_instant"),
                data.get("effective_start"),
                data.get("effective_end"),
            )
        if not data.get("content_hash"):
            # Apply the model defaults of hashed fields so the pre-computation
            # matches the post-validation recomputation exactly.
            defaults: dict[str, Any] = {
                "schema_version": SCHEMA_VERSION,
                "scale": 0,
                "derived_from_fact_ids": [],
                "corroborating_fact_ids": [],
                "revision_type": RevisionType.ORIGINAL.value,
            }
            data["content_hash"] = compute_content_hash({**defaults, **data})
        return data

    @model_validator(mode="after")
    def _invariants(self) -> InstitutionalFact:
        # Metric must be in the controlled registry (Sprint-2 vocabulary).
        spec = METRIC_REGISTRY.get(self.metric_ref)
        if spec is None:
            raise ValueError(f"metric_ref {self.metric_ref!r} is not in METRIC_REGISTRY.")
        if spec.value_type is not self.value_type:
            raise ValueError(
                f"metric_ref {self.metric_ref!r} requires value_type {spec.value_type.value}."
            )

        # World-time fields are mutually constrained.
        if self.period_type is PeriodType.INSTANT:
            if self.effective_instant is None or self.effective_start or self.effective_end:
                raise ValueError("INSTANT requires effective_instant only (no start/end).")
        else:
            if self.effective_start is None or self.effective_end is None:
                raise ValueError("DURATION requires effective_start and effective_end.")
            if self.effective_instant is not None:
                raise ValueError("DURATION must not set effective_instant.")
            if self.effective_start >= self.effective_end:
                raise ValueError("effective_start must precede effective_end.")

        # MONEY requires a currency.
        if self.value_type is ValueType.MONEY and not self.currency:
            raise ValueError("MONEY values require a currency.")

        # Lineage: DERIVED requires it; PRIMARY forbids it.
        if (
            self.assertion_type is AssertionType.DERIVED
            or self.provenance_type is ProvenanceType.DERIVED
        ) and not self.derived_from_fact_ids:
            raise ValueError("DERIVED facts require derived_from_fact_ids lineage.")
        if self.provenance_type is ProvenanceType.PRIMARY and self.derived_from_fact_ids:
            raise ValueError("PRIMARY facts cannot contain derived_from_fact_ids.")

        # MOCK can never be Verified Fact (governance: no fabricated certainty).
        if (
            self.provenance_type is ProvenanceType.MOCK
            or self.retrieval_method is RetrievalMethod.MOCK
        ) and self.knowledge_class is KnowledgeClass.VERIFIED_FACT:
            raise ValueError("MOCK facts can never be classified Verified Fact.")

        # FORECAST is never a settled report.
        if (
            self.assertion_type is AssertionType.FORECAST
            and self.knowledge_class is KnowledgeClass.VERIFIED_FACT
        ):
            raise ValueError("FORECAST facts cannot be classified Verified Fact.")

        # Revision chain sanity (acyclicity across records is enforced by the store).
        if self.supersedes_fact_id == self.fact_id:
            raise ValueError("A Fact cannot supersede itself.")
        if self.revision_type is RevisionType.ORIGINAL and self.supersedes_fact_id:
            raise ValueError("ORIGINAL facts cannot supersede another fact.")
        if self.revision_type is not RevisionType.ORIGINAL and not self.supersedes_fact_id:
            raise ValueError(f"{self.revision_type.value} requires supersedes_fact_id.")

        # Deterministic identity must verify.
        expected_key = compute_fact_key(
            self.subject_scope_type,
            self.subject_scope_id,
            self.metric_ref,
            self.basis,
            self.period_type,
            self.effective_instant,
            self.effective_start,
            self.effective_end,
        )
        if self.fact_key != expected_key:
            raise ValueError("fact_key does not match its deterministic derivation.")
        expected_hash = compute_content_hash(dict(self))
        if self.content_hash != expected_hash:
            raise ValueError("content_hash does not match canonical assertion content.")
        return self

    @property
    def usable_for_calculation(self) -> bool:
        """Content-level gate; the store adds the event-derived validation gate."""
        return (
            self.knowledge_class.usable_for_calculation
            and self.assertion_type is not AssertionType.FORECAST
        )


def canonical_value(fact: InstitutionalFact) -> float | None:
    """The value explicitly normalized to canonical scale 0, when numeric."""
    if not isinstance(fact.value, (int, float)):
        return None
    return float(fact.value) * (10**fact.scale)


# Consecutive comparable annual periods: period ends must be ~1 year apart.
_YOY_GAP_DAYS = (300, 430)


def are_comparable(
    fact_current: InstitutionalFact,
    fact_prior: InstitutionalFact,
    decision_time: datetime | None = None,
    *,
    canonical_scale: int | None = None,
) -> bool:
    """Canonical annual-comparability predicate (CRO conditions, PR #2 review).

    FAILS CLOSED: returns True only when ALL applicable conditions pass —
    same subject/scope/metric/basis/period_type/unit/currency; same scale
    (or the caller declares explicit normalization via ``canonical_scale``
    and compares through :func:`canonical_value`); period ends of consecutive
    annual periods (300-430 days apart); both facts usable for calculation;
    and, when ``decision_time`` is supplied, neither fact retrieved after it
    (a later restatement is therefore never mixed into an earlier historical
    view). Selecting the point-in-time CURRENT fact from each source stream
    is the caller's duty (see InMemoryFactStore.current_facts_as_of) — two
    facts alone cannot prove they are the current ones.
    """
    a, b = fact_current, fact_prior
    if not (a.usable_for_calculation and b.usable_for_calculation):
        return False
    if (
        a.subject_entity_id != b.subject_entity_id
        or a.subject_scope_type != b.subject_scope_type
        or a.subject_scope_id != b.subject_scope_id
        or a.metric_ref != b.metric_ref
        or a.basis != b.basis
        or a.period_type != b.period_type
        or a.unit != b.unit
        or a.currency != b.currency
    ):
        return False
    if a.scale != b.scale and canonical_scale is None:
        return False
    if decision_time is not None and (
        a.retrieved_at > decision_time or b.retrieved_at > decision_time
    ):
        return False
    end_a = a.effective_end if a.period_type == PeriodType.DURATION else a.effective_instant
    end_b = b.effective_end if b.period_type == PeriodType.DURATION else b.effective_instant
    if end_a is None or end_b is None:
        return False
    lo, hi = _YOY_GAP_DAYS
    return lo <= (end_a - end_b).days <= hi


class FactValidationEvent(BaseModel):
    """Append-only validation status event. Current status = latest event."""

    model_config = {"frozen": True}

    event_id: str = Field(default_factory=lambda: new_id("fvev"))
    fact_id: str = Field(min_length=1)
    status: ValidationStatus
    reason: str = ""
    occurred_at: datetime = Field(default_factory=utcnow)
    recorded_by: str = Field(min_length=1)


class FactFreshnessEvent(BaseModel):
    """Append-only freshness status event. Current status = latest event."""

    model_config = {"frozen": True}

    event_id: str = Field(default_factory=lambda: new_id("ffev"))
    fact_id: str = Field(min_length=1)
    status: FreshnessStatus
    reason: str = ""
    occurred_at: datetime = Field(default_factory=utcnow)
    recorded_by: str = Field(min_length=1)
