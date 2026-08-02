"""Investment Thesis (Pydantic v2) — Constitution Sec 8 schema.

Governance in code: hypothesis is mandatory (ADR-032); bear case and
invalidation are required with minimum content. Confidence lives ONLY in
Scores; recommended size lives in RiskResult (not here).
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from .base import new_id
from .enums import Direction, ThesisStatus, TimeHorizon
from .risk import RiskResult


class Scores(BaseModel):
    """Rubric scores (ARES-RISK-001). Confidence lives here, not on Thesis."""

    evidence_quality: int | None = Field(default=None, ge=0, le=100)
    thesis_completeness: int | None = Field(default=None, ge=0, le=100)
    probability: int | None = Field(default=None, ge=0, le=100)
    confidence: int | None = Field(default=None, ge=0, le=100)
    asymmetry: int | None = Field(default=None, ge=0, le=100)
    data_freshness: int | None = Field(default=None, ge=0, le=100)
    conviction: int | None = Field(default=None, ge=0, le=100)
    rubric_version: str = "unset"


class Thesis(BaseModel):
    entity_id: str = Field(min_length=1)
    thesis_summary: str = Field(min_length=1)
    hypothesis: str = Field(
        min_length=20,
        description="One testable central claim (formerly the Hypothesis entity, ADR-032).",
    )
    bear_case: str = Field(min_length=10, description="Mandatory steel-manned bear case (Sec 8).")
    invalidation_conditions: str = Field(
        min_length=3, description="Mandatory invalidation (Sec 8)."
    )
    mispricing_mechanism: str = ""
    bull_case: str = ""
    base_case: str = ""
    catalysts: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    missing_evidence: list[str] = Field(default_factory=list)
    time_horizon: TimeHorizon | None = None
    direction: Direction | None = None
    scores: Scores | None = None
    risk_result: RiskResult | None = None
    status: ThesisStatus = ThesisStatus.DRAFT
    thesis_id: str = Field(default_factory=lambda: new_id("thesis"))
    version: int = 1
