"""In-memory append-only Fact store — the smallest storage that proves the
ARES-FACT-001 design: append-only creation, status-event history, deterministic
deduplication, point-in-time queries and acyclic revision chains.

Deliberately NOT the production PostgreSQL layer (out of Sprint-2 scope).
No update or delete operation exists anywhere on this class.
"""

from __future__ import annotations

import logging
from datetime import datetime

from ares.models.base import utcnow
from ares.models.ifact import FactFreshnessEvent, FactValidationEvent, InstitutionalFact
from ares.models.vocab import FreshnessStatus, ValidationStatus

logger = logging.getLogger(__name__)


class FactStoreError(ValueError):
    """Raised when an append would violate an ARES-FACT-001 invariant."""


class InMemoryFactStore:
    """Append-only fact + status-event log with point-in-time reads."""

    def __init__(self) -> None:
        self._facts: dict[str, InstitutionalFact] = {}
        self._by_hash: dict[str, str] = {}  # content_hash -> fact_id
        self._validation_events: list[FactValidationEvent] = []
        self._freshness_events: list[FactFreshnessEvent] = []

    # ---- append-only writes -------------------------------------------------

    def append(self, fact: InstitutionalFact) -> InstitutionalFact:
        """Append a fact. Idempotent on content_hash (deterministic dedup)."""
        existing_id = self._by_hash.get(fact.content_hash)
        if existing_id is not None:
            logger.info("store: dedup hit for %s (existing %s)", fact.fact_id, existing_id)
            return self._facts[existing_id]
        if fact.fact_id in self._facts:
            raise FactStoreError(f"fact_id {fact.fact_id!r} already exists (append-only).")
        if fact.retrieved_at > utcnow():
            raise FactStoreError("retrieved_at cannot be in the future.")
        if fact.supersedes_fact_id is not None:
            if fact.supersedes_fact_id not in self._facts:
                raise FactStoreError(
                    f"supersedes_fact_id {fact.supersedes_fact_id!r} is not in the store."
                )
            self._check_chain_acyclic(fact)
        self._facts[fact.fact_id] = fact
        self._by_hash[fact.content_hash] = fact.fact_id
        return fact

    def add_validation_event(self, event: FactValidationEvent) -> FactValidationEvent:
        self._require_fact(event.fact_id)
        self._validation_events.append(event)
        return event

    def add_freshness_event(self, event: FactFreshnessEvent) -> FactFreshnessEvent:
        self._require_fact(event.fact_id)
        self._freshness_events.append(event)
        return event

    # ---- reads --------------------------------------------------------------

    def get(self, fact_id: str) -> InstitutionalFact:
        return self._require_fact(fact_id)

    def all_facts(self) -> list[InstitutionalFact]:
        return list(self._facts.values())

    def by_fact_key(self, fact_key: str) -> list[InstitutionalFact]:
        """All records sharing one logical identity (multiple sources/revisions)."""
        return [f for f in self._facts.values() if f.fact_key == fact_key]

    def facts_as_of(self, decision_time: datetime) -> list[InstitutionalFact]:
        """Point-in-time view: only facts already retrieved by decision_time.

        Nothing retrieved after decision time can leak into a historical query.
        """
        return [f for f in self._facts.values() if f.retrieved_at <= decision_time]

    def is_current(self, fact_id: str, as_of: datetime | None = None) -> bool:
        """Derived by reverse supersession lookup — never stored."""
        self._require_fact(fact_id)
        universe = self.facts_as_of(as_of) if as_of is not None else self.all_facts()
        return not any(f.supersedes_fact_id == fact_id for f in universe)

    def current_facts_as_of(self, decision_time: datetime) -> list[InstitutionalFact]:
        visible = self.facts_as_of(decision_time)
        superseded = {f.supersedes_fact_id for f in visible if f.supersedes_fact_id}
        return [f for f in visible if f.fact_id not in superseded]

    def validation_status(self, fact_id: str) -> ValidationStatus:
        """Derived: latest validation event, else PENDING."""
        self._require_fact(fact_id)
        events = [e for e in self._validation_events if e.fact_id == fact_id]
        if not events:
            return ValidationStatus.PENDING
        return max(events, key=lambda e: e.occurred_at).status

    def freshness_status(self, fact_id: str) -> FreshnessStatus:
        """Derived: latest freshness event, else FRESH."""
        self._require_fact(fact_id)
        events = [e for e in self._freshness_events if e.fact_id == fact_id]
        if not events:
            return FreshnessStatus.FRESH
        return max(events, key=lambda e: e.occurred_at).status

    def validation_history(self, fact_id: str) -> list[FactValidationEvent]:
        return [e for e in self._validation_events if e.fact_id == fact_id]

    def usable_for_calculation(self, fact_id: str) -> bool:
        """Content gate AND event-derived validation gate (VALID required)."""
        fact = self._require_fact(fact_id)
        return fact.usable_for_calculation and (
            self.validation_status(fact_id) is ValidationStatus.VALID
        )

    # ---- internals ----------------------------------------------------------

    def _require_fact(self, fact_id: str) -> InstitutionalFact:
        fact = self._facts.get(fact_id)
        if fact is None:
            raise FactStoreError(f"Unknown fact_id {fact_id!r}.")
        return fact

    def _check_chain_acyclic(self, incoming: InstitutionalFact) -> None:
        """Walk the supersession chain from the incoming fact; reject cycles."""
        seen = {incoming.fact_id}
        cursor = incoming.supersedes_fact_id
        while cursor is not None:
            if cursor in seen:
                raise FactStoreError("Revision chain would contain a cycle.")
            seen.add(cursor)
            cursor = self._facts[cursor].supersedes_fact_id if cursor in self._facts else None
