"""Fact Object — a verified, sourced, timestamped datum.

Schema: ARES-003 Sec 5.3 / ARES-015 Part B. A Fact is the ONLY form in which a
number reaches an LLM (Constitution Sec 5). A Fact is *sourced*; a Signal is
*computed* — do not confuse them.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Union

from .base import AresValidationError, new_id, require, utcnow
from .enums import KnowledgeClass


@dataclass
class Fact:
    entity_id: str
    metric_name: str
    value: Union[float, int, str]
    source_name: str
    source_id_or_url: str
    as_of_timestamp: datetime
    knowledge_class: KnowledgeClass = KnowledgeClass.VERIFIED_FACT
    unit: Optional[str] = None
    validation_status: str = "valid"
    retrieved_at: datetime = field(default_factory=utcnow)
    fact_id: str = field(default_factory=lambda: new_id("fact"))
    version: int = 1

    def __post_init__(self) -> None:
        require(bool(self.entity_id), "Fact.entity_id is required")
        require(bool(self.metric_name), "Fact.metric_name is required")
        # A Verified Fact MUST carry a real source (Constitution Sec 5).
        if self.knowledge_class == KnowledgeClass.VERIFIED_FACT:
            require(
                bool(self.source_name) and bool(self.source_id_or_url),
                "A Verified Fact requires source_name and source_id_or_url "
                "(Constitution Sec 5). Downgrade the class or add a source.",
            )

    @property
    def usable_for_calculation(self) -> bool:
        """Whether this fact may feed a deterministic calculation."""
        return (
            self.knowledge_class.usable_for_calculation
            and self.validation_status == "valid"
        )
