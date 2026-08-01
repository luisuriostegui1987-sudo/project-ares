"""Evidence & Claim.

- **Claim**: a single statement with a knowledge class and supporting /
  contradicting Fact ids (ARES-004 Sec 6).
- **Evidence**: one or more Facts (via Claims) marshaled to support or refute
  something — Facts *in service of* a conclusion (ARES-015).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .base import in_range, new_id, require
from .enums import ClaimType, KnowledgeClass

# order weakest -> strongest, for computing a conservative overall class
_CLASS_STRENGTH = [
    KnowledgeClass.UNKNOWN,
    KnowledgeClass.OPINION,
    KnowledgeClass.SPECULATION,
    KnowledgeClass.REASONABLE_INFERENCE,
    KnowledgeClass.HIGH_CONFIDENCE,
    KnowledgeClass.VERIFIED_FACT,
]


@dataclass
class Claim:
    statement: str
    knowledge_class: KnowledgeClass
    claim_type: ClaimType = ClaimType.FACTUAL
    supporting_fact_ids: List[str] = field(default_factory=list)
    contradicting_fact_ids: List[str] = field(default_factory=list)
    confidence_score: Optional[int] = None  # 0-100
    reasoning_summary: str = ""
    unresolved_questions: List[str] = field(default_factory=list)
    claim_id: str = field(default_factory=lambda: new_id("claim"))

    def __post_init__(self) -> None:
        require(bool(self.statement), "Claim.statement is required")
        require(
            in_range(self.confidence_score, 0, 100),
            "Claim.confidence_score must be within 0-100",
        )
        # A claim with no supporting evidence cannot be Verified/High (ACP Sec 6).
        if self.knowledge_class in (
            KnowledgeClass.VERIFIED_FACT,
            KnowledgeClass.HIGH_CONFIDENCE,
        ):
            require(
                len(self.supporting_fact_ids) > 0,
                "A Verified Fact / High Confidence claim needs at least one "
                "supporting_fact_id (ARES-004 Sec 6).",
            )


@dataclass
class Evidence:
    subject: str
    claims: List[Claim] = field(default_factory=list)
    supporting_fact_ids: List[str] = field(default_factory=list)
    contradicting_fact_ids: List[str] = field(default_factory=list)
    summary: str = ""
    evidence_id: str = field(default_factory=lambda: new_id("evid"))

    def __post_init__(self) -> None:
        require(bool(self.subject), "Evidence.subject is required")

    @property
    def overall_class(self) -> KnowledgeClass:
        """Conservative overall class = the weakest claim's class."""
        if not self.claims:
            return KnowledgeClass.UNKNOWN
        return min(
            (c.knowledge_class for c in self.claims),
            key=_CLASS_STRENGTH.index,
        )
