"""Evidence & Claim (Pydantic v2). Facts marshaled to support/refute a claim
(ARES-004 Sec 6 / ARES-015)."""

from __future__ import annotations

from pydantic import BaseModel, Field, model_validator

from .base import new_id
from .enums import ClaimType, KnowledgeClass

# weakest -> strongest, for a conservative overall class
_CLASS_STRENGTH = [
    KnowledgeClass.UNKNOWN,
    KnowledgeClass.OPINION,
    KnowledgeClass.SPECULATION,
    KnowledgeClass.REASONABLE_INFERENCE,
    KnowledgeClass.HIGH_CONFIDENCE,
    KnowledgeClass.VERIFIED_FACT,
]


class Claim(BaseModel):
    statement: str = Field(min_length=1)
    knowledge_class: KnowledgeClass
    claim_type: ClaimType = ClaimType.FACTUAL
    supporting_fact_ids: list[str] = Field(default_factory=list)
    contradicting_fact_ids: list[str] = Field(default_factory=list)
    confidence_score: int | None = Field(default=None, ge=0, le=100)
    reasoning_summary: str = ""
    unresolved_questions: list[str] = Field(default_factory=list)
    claim_id: str = Field(default_factory=lambda: new_id("claim"))

    @model_validator(mode="after")
    def _support(self) -> Claim:
        if (
            self.knowledge_class
            in (
                KnowledgeClass.VERIFIED_FACT,
                KnowledgeClass.HIGH_CONFIDENCE,
            )
            and not self.supporting_fact_ids
        ):
            raise ValueError(
                "A Verified Fact / High Confidence claim needs >=1 "
                "supporting_fact_id (ARES-004 Sec 6)."
            )
        return self


class Evidence(BaseModel):
    subject: str = Field(min_length=1)
    claims: list[Claim] = Field(default_factory=list)
    supporting_fact_ids: list[str] = Field(default_factory=list)
    contradicting_fact_ids: list[str] = Field(default_factory=list)
    summary: str = ""
    evidence_id: str = Field(default_factory=lambda: new_id("evid"))

    @property
    def overall_class(self) -> KnowledgeClass:
        if not self.claims:
            return KnowledgeClass.UNKNOWN
        return min((c.knowledge_class for c in self.claims), key=_CLASS_STRENGTH.index)
