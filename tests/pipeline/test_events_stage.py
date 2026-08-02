"""Stage 3 (Events) unit tests."""
from __future__ import annotations

from datetime import UTC, datetime

import pytest

from ares.models import Event, EventType
from ares.pipeline.entity import Entity, MockEntityProvider, resolve_entity
from ares.pipeline.events import MockEventsProvider, gather_events


def _nvda() -> Entity:
    return resolve_entity("NVDA", MockEntityProvider())


def test_events_gathered_and_sorted():
    events = gather_events(_nvda(), MockEventsProvider())
    assert len(events) == 2
    assert events == sorted(events, key=lambda e: e.occurs_at)
    assert any(e.is_catalyst for e in events)


def test_unknown_entity_yields_no_events():
    entity = Entity(entity_id="AAPL", ticker="AAPL", name="Apple Inc.")
    assert gather_events(entity, MockEventsProvider()) == []


def test_foreign_events_rejected():
    class BadProvider:
        def events_for(self, entity: Entity) -> list[Event]:
            return [
                Event(
                    entity_id="OTHER",
                    event_type=EventType.OTHER,
                    title="not yours",
                    occurs_at=datetime(2026, 9, 1, tzinfo=UTC),
                )
            ]

    with pytest.raises(ValueError, match="do not belong"):
        gather_events(_nvda(), BadProvider())
