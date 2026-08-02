"""Stage 4 — Facts: sourced, timestamped data points for an Entity.

Input:  Entity.
Output: list[Fact] (domain model).

A Fact is the ONLY form in which a number enters the pipeline (Constitution
Sec 5). Mock facts are explicitly labeled with mock:// sources so they can
never be mistaken for real market data.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import ClassVar, Protocol

from ares.models import Fact, KnowledgeClass

from .entity import Entity

logger = logging.getLogger(__name__)

# Canonical metric names the Sprint-1 signal rules understand.
METRIC_REVENUE_TTM_CURRENT = "revenue_ttm_current_usd"
METRIC_REVENUE_TTM_PRIOR = "revenue_ttm_prior_year_usd"
METRIC_GROSS_MARGIN_PCT = "gross_margin_pct"


class FactsProvider(Protocol):
    def facts_for(self, entity: Entity) -> list[Fact]: ...


class MockFactsProvider:
    """Static, clearly-labeled mock financials for the Sprint-1 slice."""

    _AS_OF = datetime(2026, 7, 31, tzinfo=UTC)

    _ROWS: ClassVar[dict[str, list[tuple[str, float, str]]]] = {
        # (metric_name, value, unit)
        "NVDA": [
            (METRIC_REVENUE_TTM_CURRENT, 165_200_000_000.0, "USD"),
            (METRIC_REVENUE_TTM_PRIOR, 113_300_000_000.0, "USD"),
            (METRIC_GROSS_MARGIN_PCT, 74.9, "%"),
        ],
        "CRWV": [
            (METRIC_REVENUE_TTM_CURRENT, 4_500_000_000.0, "USD"),
            (METRIC_REVENUE_TTM_PRIOR, 1_900_000_000.0, "USD"),
            (METRIC_GROSS_MARGIN_PCT, 61.0, "%"),
        ],
    }

    def facts_for(self, entity: Entity) -> list[Fact]:
        rows = self._ROWS.get(entity.entity_id, [])
        return [
            Fact(
                entity_id=entity.entity_id,
                metric_name=metric,
                value=value,
                unit=unit,
                source_name="MOCK provider (Sprint-1 slice)",
                source_id_or_url=f"mock://facts/{entity.entity_id.lower()}/{metric}",
                as_of_timestamp=self._AS_OF,
                knowledge_class=KnowledgeClass.HIGH_CONFIDENCE,
            )
            for metric, value, unit in rows
        ]


def gather_facts(entity: Entity, provider: FactsProvider) -> list[Fact]:
    """Fetch facts and validate ownership + calculation usability."""
    facts = provider.facts_for(entity)
    foreign = [f.fact_id for f in facts if f.entity_id != entity.entity_id]
    if foreign:
        raise ValueError(f"Facts {foreign} do not belong to entity {entity.entity_id!r}.")
    usable = sum(1 for f in facts if f.usable_for_calculation)
    if facts and usable == 0:
        logger.warning(
            "facts: none of the %d facts for %s are usable for calculation",
            len(facts),
            entity.entity_id,
        )
    logger.info("facts: %d gathered for %s (%d usable)", len(facts), entity.entity_id, usable)
    return facts
