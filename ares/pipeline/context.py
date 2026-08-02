"""Stage 2 — Context: qualitative business context for a resolved Entity.

Input:  Entity.
Output: EntityContext — what the business is, so later stages read facts in context.

Context is descriptive prose/metadata, NOT numbers. Numbers must arrive as
Fact objects (Constitution Sec 5) in the Facts stage.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import ClassVar, Protocol

from pydantic import BaseModel, Field

from ares.models.base import utcnow

from .entity import Entity

logger = logging.getLogger(__name__)


class EntityContext(BaseModel):
    """Business context for one entity (qualitative only)."""

    entity_id: str = Field(min_length=1)
    business_summary: str = Field(min_length=1)
    key_products: list[str] = Field(default_factory=list)
    competitors: list[str] = Field(default_factory=list)
    as_of: datetime = Field(default_factory=utcnow)


class ContextProvider(Protocol):
    def context_for(self, entity: Entity) -> EntityContext: ...


class MockContextProvider:
    """Static context for the Sprint-1 slice."""

    _SUMMARIES: ClassVar[dict[str, dict[str, object]]] = {
        "NVDA": {
            "business_summary": (
                "Designs GPUs and full-stack accelerated-computing platforms; "
                "dominant supplier of AI datacenter compute."
            ),
            "key_products": ["Data Center GPUs", "CUDA platform", "Networking (Mellanox)"],
            "competitors": ["AMD", "Intel", "Custom silicon (TPU/Trainium)"],
        },
        "CRWV": {
            "business_summary": (
                "AI-focused cloud provider renting GPU capacity at scale; "
                "customer-concentrated, capex-heavy growth model."
            ),
            "key_products": ["GPU cloud instances", "Managed AI clusters"],
            "competitors": ["AWS", "Azure", "Lambda", "Nebius"],
        },
        "AAPL": {
            "business_summary": "Consumer hardware, services and ecosystem company.",
            "key_products": ["iPhone", "Services", "Mac"],
            "competitors": ["Samsung", "Google"],
        },
    }

    def context_for(self, entity: Entity) -> EntityContext:
        row = self._SUMMARIES.get(entity.entity_id)
        if row is None:
            raise LookupError(f"No context available for {entity.entity_id!r}.")
        return EntityContext(entity_id=entity.entity_id, **row)  # type: ignore[arg-type]


def build_context(entity: Entity, provider: ContextProvider) -> EntityContext:
    """Fetch and validate context for the entity."""
    ctx = provider.context_for(entity)
    if ctx.entity_id != entity.entity_id:
        raise ValueError(
            f"Context entity_id {ctx.entity_id!r} does not match entity {entity.entity_id!r}."
        )
    logger.info(
        "context: built for %s (%d products, %d competitors)",
        entity.entity_id,
        len(ctx.key_products),
        len(ctx.competitors),
    )
    return ctx
