"""Stage 1 — Entity resolution: a raw ticker becomes a validated Entity.

Input:  ticker string (e.g. "NVDA").
Output: Entity (canonical model in ares.models.entity).

Providers are swappable: MockEntityProvider ships now; a real reference-data
provider implements the same EntityProvider protocol later.
"""

from __future__ import annotations

import logging
from typing import ClassVar, Protocol

from ares.models import Entity
from ares.models.entity import TICKER_RE

logger = logging.getLogger(__name__)


class EntityProvider(Protocol):
    """Anything that can resolve a normalized ticker into an Entity."""

    def resolve(self, ticker: str) -> Entity: ...


class MockEntityProvider:
    """Static reference data for the Sprint-1 slice. Replace with a real provider later."""

    _KNOWN: ClassVar[dict[str, dict[str, str]]] = {
        "NVDA": {
            "name": "NVIDIA Corporation",
            "exchange": "NASDAQ",
            "sector": "Information Technology",
            "industry": "Semiconductors",
        },
        "CRWV": {
            "name": "CoreWeave, Inc.",
            "exchange": "NASDAQ",
            "sector": "Information Technology",
            "industry": "AI Cloud Infrastructure",
        },
        "AAPL": {
            "name": "Apple Inc.",
            "exchange": "NASDAQ",
            "sector": "Information Technology",
            "industry": "Consumer Electronics",
        },
    }

    def resolve(self, ticker: str) -> Entity:
        row = self._KNOWN.get(ticker)
        if row is None:
            raise LookupError(f"Unknown entity: {ticker!r} (mock universe: {sorted(self._KNOWN)}).")
        return Entity(entity_id=ticker, ticker=ticker, **row)


def resolve_entity(ticker: str, provider: EntityProvider) -> Entity:
    """Normalize + validate the ticker, then resolve it through the provider."""
    normalized = ticker.strip().upper()
    if not TICKER_RE.match(normalized):
        raise ValueError(f"Invalid ticker: {ticker!r}.")
    entity = provider.resolve(normalized)
    if entity.entity_id != normalized:
        raise ValueError(
            f"Provider returned entity_id {entity.entity_id!r} for ticker {normalized!r}."
        )
    logger.info("entity: resolved %s -> %s", normalized, entity.name)
    return entity
