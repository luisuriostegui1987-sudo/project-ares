"""Research Pipeline orchestrator — runs the approved stage sequence.

    Entity -> Context -> Events -> Facts -> Evidence -> Signals -> ResearchReport

Providers default to the Sprint-1 mocks; inject real implementations of the
same protocols to go live. No Risk, no Decision, no Portfolio in this slice.
"""
from __future__ import annotations

import logging

from .context import ContextProvider, MockContextProvider, build_context
from .entity import EntityProvider, MockEntityProvider, resolve_entity
from .events import EventsProvider, MockEventsProvider, gather_events
from .evidence import derive_evidence
from .facts import FactsProvider, MockFactsProvider, gather_facts
from .output import ResearchReport
from .signals import derive_signals

logger = logging.getLogger(__name__)


class ResearchPipeline:
    """Sequential, provider-injectable research pipeline (ARES-003 Sec 14 slice)."""

    def __init__(
        self,
        entity_provider: EntityProvider | None = None,
        context_provider: ContextProvider | None = None,
        events_provider: EventsProvider | None = None,
        facts_provider: FactsProvider | None = None,
    ) -> None:
        self.entity_provider = entity_provider or MockEntityProvider()
        self.context_provider = context_provider or MockContextProvider()
        self.events_provider = events_provider or MockEventsProvider()
        self.facts_provider = facts_provider or MockFactsProvider()

    def run(self, ticker: str) -> ResearchReport:
        """Execute every stage in order and return the validated report."""
        logger.info("pipeline: run started for %r", ticker)
        entity = resolve_entity(ticker, self.entity_provider)
        context = build_context(entity, self.context_provider)
        events = gather_events(entity, self.events_provider)
        facts = gather_facts(entity, self.facts_provider)
        evidence = derive_evidence(entity, facts)
        signals = derive_signals(entity, facts)
        report = ResearchReport(
            entity=entity,
            context=context,
            events=events,
            facts=facts,
            evidence=evidence,
            signals=signals,
        )
        logger.info("pipeline: run complete for %s (report %s)", entity.entity_id, report.report_id)
        return report
