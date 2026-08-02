"""Stage 2 (Context) unit tests."""
from __future__ import annotations

import pytest

from ares.pipeline.context import EntityContext, MockContextProvider, build_context
from ares.pipeline.entity import Entity, MockEntityProvider, resolve_entity


def _nvda() -> Entity:
    return resolve_entity("NVDA", MockEntityProvider())


def test_context_built_for_known_entity():
    ctx = build_context(_nvda(), MockContextProvider())
    assert ctx.entity_id == "NVDA"
    assert "GPU" in ctx.business_summary or "GPUs" in ctx.business_summary
    assert ctx.key_products


def test_context_entity_mismatch_rejected():
    class BadProvider:
        def context_for(self, entity: Entity) -> EntityContext:
            return EntityContext(entity_id="OTHER", business_summary="wrong")

    with pytest.raises(ValueError, match="does not match"):
        build_context(_nvda(), BadProvider())


def test_context_unknown_entity_raises():
    entity = Entity(entity_id="ZZZZ", ticker="ZZZZ", name="Zed Corp")
    with pytest.raises(LookupError):
        build_context(entity, MockContextProvider())
