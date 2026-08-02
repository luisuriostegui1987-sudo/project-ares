"""Stage 3 — Events: known past/upcoming events (catalysts included) for an Entity.

Input:  Entity.
Output: list[Event] (domain model), sorted by occurs_at.

The Event/catalyst semantics live in ares.models.event; this stage only
gathers and validates them.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Protocol

from ares.models import Direction, Event, EventType

from .entity import Entity

logger = logging.getLogger(__name__)


class EventsProvider(Protocol):
    def events_for(self, entity: Entity) -> list[Event]: ...


class MockEventsProvider:
    """Static event calendar for the Sprint-1 slice."""

    def events_for(self, entity: Entity) -> list[Event]:
        if entity.entity_id == "NVDA":
            return [
                Event(
                    entity_id="NVDA",
                    event_type=EventType.EARNINGS,
                    title="Q2 FY2027 earnings report",
                    occurs_at=datetime(2026, 8, 26, 21, 0, tzinfo=UTC),
                    is_catalyst=True,
                    expected_direction=Direction.LONG,
                    expected_effect="High-impact print; AI datacenter demand read-through.",
                ),
                Event(
                    entity_id="NVDA",
                    event_type=EventType.PRODUCT_LAUNCH,
                    title="Next-gen datacenter GPU architecture update (GTC)",
                    occurs_at=datetime(2026, 10, 6, 17, 0, tzinfo=UTC),
                    is_catalyst=False,
                ),
            ]
        if entity.entity_id == "CRWV":
            return [
                Event(
                    entity_id="CRWV",
                    event_type=EventType.EARNINGS,
                    title="Q2 2026 earnings report",
                    occurs_at=datetime(2026, 8, 11, 20, 0, tzinfo=UTC),
                    is_catalyst=True,
                    expected_effect="High-impact print for a young, volatile name.",
                ),
            ]
        return []


def gather_events(entity: Entity, provider: EventsProvider) -> list[Event]:
    """Fetch events, validate ownership, and return them sorted by occurs_at."""
    events = provider.events_for(entity)
    foreign = [e.event_id for e in events if e.entity_id != entity.entity_id]
    if foreign:
        raise ValueError(f"Events {foreign} do not belong to entity {entity.entity_id!r}.")
    ordered = sorted(events, key=lambda e: e.occurs_at)
    logger.info(
        "events: %d gathered for %s (%d catalysts)",
        len(ordered),
        entity.entity_id,
        sum(1 for e in ordered if e.is_catalyst),
    )
    return ordered
