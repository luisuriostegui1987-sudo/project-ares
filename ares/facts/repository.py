"""FactRepository — the storage abstraction for ARES-FACT-001 records.

Business logic depends ONLY on this Protocol. InMemoryFactStore and
PostgresFactRepository are interchangeable implementations; both must uphold
every invariant: immutable facts, append-only status events, deterministic
dedup on content_hash, acyclic supersession, and point-in-time reads.
"""

from __future__ import annotations

from datetime import datetime
from typing import Protocol, runtime_checkable

from ares.models.ifact import FactFreshnessEvent, FactValidationEvent, InstitutionalFact
from ares.models.vocab import FreshnessStatus, ValidationStatus


@runtime_checkable
class FactRepository(Protocol):
    """Append-only fact + status-event log with point-in-time reads."""

    # ---- append-only writes (no update/delete exists anywhere) -------------

    def append(self, fact: InstitutionalFact) -> InstitutionalFact: ...

    def add_validation_event(self, event: FactValidationEvent) -> FactValidationEvent: ...

    def add_freshness_event(self, event: FactFreshnessEvent) -> FactFreshnessEvent: ...

    # ---- reads --------------------------------------------------------------

    def get(self, fact_id: str) -> InstitutionalFact: ...

    def all_facts(self) -> list[InstitutionalFact]: ...

    def by_fact_key(self, fact_key: str) -> list[InstitutionalFact]: ...

    def facts_as_of(self, decision_time: datetime) -> list[InstitutionalFact]: ...

    def is_current(self, fact_id: str, as_of: datetime | None = None) -> bool: ...

    def current_facts_as_of(self, decision_time: datetime) -> list[InstitutionalFact]: ...

    def validation_status(self, fact_id: str) -> ValidationStatus: ...

    def freshness_status(self, fact_id: str) -> FreshnessStatus: ...

    def validation_history(self, fact_id: str) -> list[FactValidationEvent]: ...

    def usable_for_calculation(self, fact_id: str) -> bool: ...
