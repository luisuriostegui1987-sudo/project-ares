"""Investment Thesis — Constitution Sec 8 schema (ARES-003 Sec 5.6 / ARES-015).

This model encodes governance IN CODE: a thesis without a steel-manned bear
case or an invalidation condition is *rejected at construction*, not merely
discouraged. That is the Constitution enforced by the type system.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .base import in_range, new_id, require
from .enums import Direction, RiskVerdict, ThesisStatus, TimeHorizon


@dataclass
class Scores:
    """Reproducible rubric scores (ARES-003 Sec 5.8). All 0-100, optional."""

    evidence_quality: Optional[int] = None
    thesis_completeness: Optional[int] = None
    probability: Optional[int] = None
    confidence: Optional[int] = None
    asymmetry: Optional[int] = None
    data_freshness: Optional[int] = None
    rubric_version: str = "unset"

    def __post_init__(self) -> None:
        for name in (
            "evidence_quality",
            "thesis_completeness",
            "probability",
            "confidence",
            "asymmetry",
            "data_freshness",
        ):
            require(
                in_range(getattr(self, name), 0, 100),
                f"Scores.{name} must be within 0-100",
            )


@dataclass
class Thesis:
    entity_id: str
    thesis_summary: str
    bear_case: str          # MANDATORY (Constitution Sec 8)
    invalidation_conditions: str  # MANDATORY (Constitution Sec 8)
    hypothesis: str = ""   # the single testable claim; formerly the Hypothesis entity (ADR-032)
    mispricing_mechanism: str = ""
    bull_case: str = ""
    base_case: str = ""
    catalysts: List[str] = field(default_factory=list)      # Event ids
    evidence_refs: List[str] = field(default_factory=list)  # Fact / Evidence ids
    missing_evidence: List[str] = field(default_factory=list)
    time_horizon: Optional[TimeHorizon] = None
    direction: Optional[Direction] = None
    scores: Optional[Scores] = None
    risk_result: Optional[RiskVerdict] = None
    confidence: Optional[int] = None      # 0-100
    position_size: Optional[float] = None  # paper size; 0 = watchlist
    status: ThesisStatus = ThesisStatus.DRAFT
    thesis_id: str = field(default_factory=lambda: new_id("thesis"))
    version: int = 1

    def __post_init__(self) -> None:
        require(bool(self.entity_id), "Thesis.entity_id is required")
        require(bool(self.thesis_summary), "Thesis.thesis_summary is required")
        # The two rules that make ARES ARES:
        require(
            len(self.bear_case.strip()) >= 10,
            "A thesis without a real bear case is rejected (Constitution Sec 8).",
        )
        require(
            len(self.invalidation_conditions.strip()) >= 3,
            "A thesis without an invalidation condition is rejected "
            "(Constitution Sec 8).",
        )
        require(
            in_range(self.confidence, 0, 100),
            "Thesis.confidence must be within 0-100",
        )
