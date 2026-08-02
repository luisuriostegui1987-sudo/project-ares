"""Fact Object — a verified, sourced, timestamped datum (ARES-003 Sec 5.3 / ARES-015).

A Fact is the ONLY form in which a number reaches an LLM (Constitution Sec 5).
A Fact is *sourced*; a Signal is *computed* — do not confuse them.
"""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from .base import new_id, utcnow
from .enums import KnowledgeClass


class Fact(BaseModel):
    entity_id: str = Field(min_length=1)
    metric_name: str = Field(min_length=1)
    value: float | int | str
    source_name: str
    source_id_or_url: str
    as_of_timestamp: datetime
    knowledge_class: KnowledgeClass = KnowledgeClass.VERIFIED_FACT
    unit: str | None = None
    validation_status: str = "valid"
    retrieved_at: datetime = Field(default_factory=utcnow)
    fact_id: str = Field(default_factory=lambda: new_id("fact"))
    version: int = 1

    @model_validator(mode="after")
    def _verified_needs_source(self) -> Fact:
        if self.knowledge_class == KnowledgeClass.VERIFIED_FACT and not (
            self.source_name and self.source_id_or_url
        ):
            raise ValueError(
                "A Verified Fact requires source_name and source_id_or_url "
                "(Constitution Sec 5)."
            )
        return self

    @property
    def usable_for_calculation(self) -> bool:
        return (
            self.knowledge_class.usable_for_calculation
            and self.validation_status == "valid"
        )
