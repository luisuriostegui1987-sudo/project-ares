"""Stage 1 (Entity) unit tests."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from ares.pipeline.entity import Entity, MockEntityProvider, resolve_entity


def test_resolves_known_ticker_case_insensitively():
    entity = resolve_entity(" nvda ", MockEntityProvider())
    assert entity.entity_id == "NVDA"
    assert entity.name == "NVIDIA Corporation"
    assert entity.sector == "Information Technology"


def test_invalid_ticker_rejected():
    with pytest.raises(ValueError, match="Invalid ticker"):
        resolve_entity("nv da!", MockEntityProvider())


def test_unknown_ticker_raises_lookup_error():
    with pytest.raises(LookupError, match="Unknown entity"):
        resolve_entity("ZZZZ", MockEntityProvider())


def test_entity_model_validates_ticker_format():
    with pytest.raises(ValidationError):
        Entity(entity_id="x", ticker="bad ticker", name="X Corp")


def test_provider_entity_id_mismatch_rejected():
    class BadProvider:
        def resolve(self, ticker: str) -> Entity:
            return Entity(entity_id="OTHER", ticker="OTHER", name="Wrong Corp")

    with pytest.raises(ValueError, match="entity_id"):
        resolve_entity("NVDA", BadProvider())
