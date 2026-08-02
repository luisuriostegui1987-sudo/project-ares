"""Research Pipeline orchestrator — runs the approved stage sequence.

    Entity -> Context -> Events -> Facts -> Evidence -> Signals -> ResearchReport

Provider selection is explicit via DataMode:
- MOCK: Sprint-1 mock providers; output is loudly labeled mock.
- LIVE: SEC EDGAR providers; failures raise — a live run NEVER silently
  substitutes mock data (guarded structurally below).
"""

from __future__ import annotations

import logging

from .context import ContextProvider, MockContextProvider, build_context
from .entity import EntityProvider, MockEntityProvider, resolve_entity
from .events import EventsProvider, MockEventsProvider, gather_events
from .evidence import derive_evidence
from .facts import FactsProvider, MockFactsProvider, gather_facts
from .output import DataMode, ResearchReport
from .signals import derive_signals

logger = logging.getLogger(__name__)


class ResearchPipeline:
    """Sequential, provider-injectable research pipeline (ARES-003 Sec 14)."""

    def __init__(
        self,
        entity_provider: EntityProvider | None = None,
        context_provider: ContextProvider | None = None,
        events_provider: EventsProvider | None = None,
        facts_provider: FactsProvider | None = None,
        data_mode: DataMode = DataMode.MOCK,
    ) -> None:
        self.data_mode = data_mode
        if data_mode is DataMode.LIVE:
            # Imported here so MOCK mode never needs the network stack.
            from ares.providers.edgar import (
                EdgarClient,
                EdgarEntityProvider,
                EdgarFactsProvider,
                LiveContextProvider,
                NoEventsProvider,
            )

            client = EdgarClient()
            self.entity_provider = entity_provider or EdgarEntityProvider(client)
            self.context_provider = context_provider or LiveContextProvider(client)
            self.events_provider = events_provider or NoEventsProvider()
            self.facts_provider = facts_provider or EdgarFactsProvider(client)
        else:
            self.entity_provider = entity_provider or MockEntityProvider()
            self.context_provider = context_provider or MockContextProvider()
            self.events_provider = events_provider or MockEventsProvider()
            self.facts_provider = facts_provider or MockFactsProvider()
        if data_mode is DataMode.LIVE:
            self._reject_mock_providers()

    def _reject_mock_providers(self) -> None:
        """A LIVE run must never contain a mock provider — fail loudly, never fall back."""
        offenders = [
            type(p).__name__
            for p in (
                self.entity_provider,
                self.context_provider,
                self.events_provider,
                self.facts_provider,
            )
            if type(p).__name__.startswith("Mock")
        ]
        if offenders:
            raise ValueError(f"LIVE mode cannot use mock providers: {offenders}.")

    def run(self, ticker: str) -> ResearchReport:
        """Execute every stage in order and return the validated report."""
        logger.info("pipeline: run started for %r (mode=%s)", ticker, self.data_mode.value)
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
            data_mode=self.data_mode,
        )
        logger.info("pipeline: run complete for %s (report %s)", entity.entity_id, report.report_id)
        return report
