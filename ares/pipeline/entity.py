"""Stage 1 — Entity resolution: a raw ticker becomes a validated Entity.

Input:  ticker string (e.g. "NVDA").
Output: Entity — the resolved instrument every later stage keys on.

Providers are swappable: MockEntityProvider ships now; a real reference-data
provider implements the same EntityProvider protocol later.
"""

from __future__ import annotations

import logging
import re
from typing import ClassVar, Protocol

from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)

_TICKER_RE = re.compile(r"^[A-Z][A-Z0-9.\-]{0,9}$")


class Entity(BaseModel):
    """A resolved, analyzable listed company (ARES-015: Entity)."""

    entity_id: str = Field(min_length=1, description="Canonical id; v1 uses the ticker itself.")
    ticker: str
    name: str = Field(min_length=1)
    exchange: str | None = None
    sector: str | None = None
    industry: str | None = None

    @field_validator("ticker")
    @classmethod
    def _ticker_format(cls, v: str) -> str:
        if not _TICKER_RE.match(v):
            raise ValueError(f"Invalid ticker format: {v!r} (expected e.g. 'NVDA', 'BRK.B').")
        return v


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
    if not _TICKER_RE.match(normalized):
        raise ValueError(f"Invalid ticker: {ticker!r}.")
    entity = provider.resolve(normalized)
    if entity.entity_id != normalized:
        raise ValueError(
            f"Provider returned entity_id {entity.entity_id!r} for ticker {normalized!r}."
        )
    logger.info("entity: resolved %s -> %s", normalized, entity.name)
    return entity
