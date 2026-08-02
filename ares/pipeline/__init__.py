"""ARES research pipeline (Sprint-1 vertical slice).

Stage order (approved): Entity -> Context -> Events -> Facts -> Evidence ->
Signals -> Structured Research Output. Depends on ares.models; never the
other way around.
"""
from .context import ContextProvider, EntityContext, MockContextProvider, build_context
from .entity import Entity, EntityProvider, MockEntityProvider, resolve_entity
from .events import EventsProvider, MockEventsProvider, gather_events
from .evidence import derive_evidence
from .facts import FactsProvider, MockFactsProvider, gather_facts
from .orchestrator import ResearchPipeline
from .output import PIPELINE_VERSION, ResearchReport, render_text
from .signals import derive_signals

__all__ = [
    "PIPELINE_VERSION",
    "ContextProvider",
    "Entity",
    "EntityContext",
    "EntityProvider",
    "EventsProvider",
    "FactsProvider",
    "MockContextProvider",
    "MockEntityProvider",
    "MockEventsProvider",
    "MockFactsProvider",
    "ResearchPipeline",
    "ResearchReport",
    "build_context",
    "derive_evidence",
    "derive_signals",
    "gather_events",
    "gather_facts",
    "render_text",
    "resolve_entity",
]
