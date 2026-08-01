"""Event — something that happened or will happen.

A **Catalyst** is an Event expected to move price or force recognition
(``is_catalyst=True``). Every Catalyst is an Event; not every Event is a
Catalyst (ARES-015).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from .base import new_id, require
from .enums import Direction, EventType


@dataclass
class Event:
    entity_id: str
    event_type: EventType
    title: str
    occurs_at: datetime  # may be past (occurred) or future (scheduled)
    is_catalyst: bool = False
    expected_direction: Optional[Direction] = None
    expected_effect: Optional[str] = None
    source_fact_ids: List[str] = field(default_factory=list)
    event_id: str = field(default_factory=lambda: new_id("event"))
    version: int = 1

    def __post_init__(self) -> None:
        require(bool(self.entity_id), "Event.entity_id is required")
        require(bool(self.title), "Event.title is required")
        # A catalyst asserts an expected effect; force it to be explicit.
        if self.is_catalyst:
            require(
                self.expected_direction is not None or bool(self.expected_effect),
                "A catalyst (is_catalyst=True) must state expected_direction "
                "or expected_effect.",
            )

    @property
    def is_future(self) -> bool:
        from .base import utcnow

        return self.occurs_at > utcnow()
