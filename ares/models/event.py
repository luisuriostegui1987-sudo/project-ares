"""Event — something that happened or will happen; a Catalyst is an Event
expected to move price (ARES-015)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from .base import new_id, utcnow
from .enums import Direction, EventType


class Event(BaseModel):
    entity_id: str = Field(min_length=1)
    event_type: EventType
    title: str = Field(min_length=1)
    occurs_at: datetime
    is_catalyst: bool = False
    expected_direction: Direction | None = None
    expected_effect: str | None = None
    source_fact_ids: list[str] = Field(default_factory=list)
    event_id: str = Field(default_factory=lambda: new_id("event"))
    version: int = 1

    @model_validator(mode="after")
    def _catalyst_needs_effect(self) -> "Event":
        if self.is_catalyst and self.expected_direction is None and not self.expected_effect:
            raise ValueError("A catalyst must state expected_direction or expected_effect.")
        return self

    @property
    def is_future(self) -> bool:
        return self.occurs_at > utcnow()
