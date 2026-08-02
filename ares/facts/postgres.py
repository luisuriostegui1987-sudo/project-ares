"""PostgresFactRepository — persistent ARES-FACT-001 store (Sprint 3).

One implementation of FactRepository; ALL SQL lives in this module. The
canonical InstitutionalFact JSON is stored verbatim in a JSONB column and
re-validated by the Pydantic model on every read, so identity invariants
(fact_key / content_hash) are verified round-trip and no migration can
silently alter the contract. Append-only is enforced twice: no mutating
method exists here, and database triggers reject UPDATE/DELETE outright.

Requires the optional dependency: pip install 'ares-core[postgres]'.
Connection DSN comes from the caller (e.g. the ARES_PG_DSN environment
variable) — never hardcoded.
"""

from __future__ import annotations

import logging
from datetime import datetime
from importlib import resources
from typing import Any

from ares.models.base import utcnow
from ares.models.ifact import FactFreshnessEvent, FactValidationEvent, InstitutionalFact
from ares.models.vocab import FreshnessStatus, ValidationStatus

from .store import FactStoreError

try:
    import psycopg
except ImportError:  # pragma: no cover - exercised only without the extra
    psycopg = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)

_MIGRATIONS = ("0001_institutional_facts.sql", "0002_research_reports.sql")


def _parse_record(raw: Any) -> InstitutionalFact:
    """JSONB may arrive as parsed dict (psycopg3 default) or as a JSON string."""
    if isinstance(raw, (str, bytes)):
        return InstitutionalFact.model_validate_json(raw)
    return InstitutionalFact.model_validate(raw)


# Deterministic advisory-lock key specific to ARES migrations ("ARES" in hex).
# pg_advisory_xact_lock is transaction-scoped: it is ALWAYS released when the
# transaction commits or rolls back — no explicit cleanup can be forgotten.
MIGRATION_LOCK_KEY = 0x41524553


def apply_migrations(conn: Any) -> list[str]:
    """Apply pending SQL migrations in order; record them in schema_migrations.

    Concurrency-safe: discovery and execution run under a transaction-scoped
    advisory lock, so two processes initializing a fresh database serialize —
    one applies, the other observes the recorded version and no-ops.
    """
    applied: list[str] = []
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT pg_advisory_xact_lock(%s)", (MIGRATION_LOCK_KEY,))
            cur.execute(
                "CREATE TABLE IF NOT EXISTS schema_migrations ("
                " version TEXT PRIMARY KEY,"
                " applied_at TIMESTAMPTZ NOT NULL DEFAULT now())"
            )
            for name in _MIGRATIONS:
                cur.execute("SELECT 1 FROM schema_migrations WHERE version = %s", (name,))
                if cur.fetchone():
                    continue
                sql = resources.files("ares.facts.migrations").joinpath(name).read_text("utf-8")
                cur.execute(sql)
                cur.execute("INSERT INTO schema_migrations (version) VALUES (%s)", (name,))
                applied.append(name)
    except Exception:
        conn.rollback()  # releases the advisory lock
        raise
    conn.commit()  # releases the advisory lock
    return applied


class PostgresFactRepository:
    """FactRepository backed by PostgreSQL. Append-only by construction and by trigger."""

    def __init__(self, dsn: str) -> None:
        if psycopg is None:
            raise RuntimeError(
                "PostgresFactRepository requires psycopg; install 'ares-core[postgres]'."
            )
        self._conn = psycopg.connect(dsn)
        applied = apply_migrations(self._conn)
        if applied:
            logger.info("postgres: applied migrations %s", applied)

    def close(self) -> None:
        self._conn.close()

    # ---- append-only writes -------------------------------------------------

    def append(self, fact: InstitutionalFact) -> InstitutionalFact:
        try:
            return self._append_inner(fact)
        except Exception:
            self._conn.rollback()
            raise

    def _append_inner(self, fact: InstitutionalFact) -> InstitutionalFact:
        with self._conn.cursor() as cur:
            cur.execute(
                "SELECT record FROM institutional_facts WHERE content_hash = %s",
                (fact.content_hash,),
            )
            row = cur.fetchone()
            if row is not None:
                existing = _parse_record(row[0])
                logger.info(
                    "postgres: dedup hit for %s (existing %s)", fact.fact_id, existing.fact_id
                )
                return existing
            cur.execute("SELECT 1 FROM institutional_facts WHERE fact_id = %s", (fact.fact_id,))
            if cur.fetchone():
                raise FactStoreError(f"fact_id {fact.fact_id!r} already exists (append-only).")
            if fact.retrieved_at > utcnow():
                raise FactStoreError("retrieved_at cannot be in the future.")
            if fact.supersedes_fact_id is not None:
                cur.execute(
                    "SELECT 1 FROM institutional_facts WHERE fact_id = %s",
                    (fact.supersedes_fact_id,),
                )
                if not cur.fetchone():
                    raise FactStoreError(
                        f"supersedes_fact_id {fact.supersedes_fact_id!r} is not in the store."
                    )
                self._check_chain_acyclic(cur, fact)
            # ON CONFLICT makes concurrent inserts of the same exact source
            # record deterministic: the first committed row wins, and any
            # concurrent loser receives the winner's record (identical to the
            # sequential dedup semantics).
            cur.execute(
                "INSERT INTO institutional_facts"
                " (fact_id, fact_key, content_hash, supersedes_fact_id, retrieved_at, record)"
                " VALUES (%s, %s, %s, %s, %s, %s)"
                " ON CONFLICT (content_hash) DO NOTHING",
                (
                    fact.fact_id,
                    fact.fact_key,
                    fact.content_hash,
                    fact.supersedes_fact_id,
                    fact.retrieved_at,
                    fact.model_dump_json(),
                ),
            )
            if cur.rowcount == 0:  # lost a concurrent race: return the winner
                self._conn.commit()
                cur.execute(
                    "SELECT record FROM institutional_facts WHERE content_hash = %s",
                    (fact.content_hash,),
                )
                winner = cur.fetchone()
                if winner is None:  # pragma: no cover - defensive
                    raise FactStoreError("Concurrent insert lost and winner not found.")
                return _parse_record(winner[0])
        self._conn.commit()
        return fact

    def add_validation_event(self, event: FactValidationEvent) -> FactValidationEvent:
        self._insert_event("fact_validation_events", event)
        return event

    def add_freshness_event(self, event: FactFreshnessEvent) -> FactFreshnessEvent:
        self._insert_event("fact_freshness_events", event)
        return event

    # ---- reads --------------------------------------------------------------

    def get(self, fact_id: str) -> InstitutionalFact:
        with self._conn.cursor() as cur:
            cur.execute("SELECT record FROM institutional_facts WHERE fact_id = %s", (fact_id,))
            row = cur.fetchone()
        if row is None:
            raise FactStoreError(f"Unknown fact_id {fact_id!r}.")
        return _parse_record(row[0])

    def all_facts(self) -> list[InstitutionalFact]:
        return self._select_facts("SELECT record FROM institutional_facts ORDER BY fact_id", ())

    def by_fact_key(self, fact_key: str) -> list[InstitutionalFact]:
        return self._select_facts(
            "SELECT record FROM institutional_facts WHERE fact_key = %s ORDER BY fact_id",
            (fact_key,),
        )

    def facts_as_of(self, decision_time: datetime) -> list[InstitutionalFact]:
        return self._select_facts(
            "SELECT record FROM institutional_facts WHERE retrieved_at <= %s ORDER BY fact_id",
            (decision_time,),
        )

    def is_current(self, fact_id: str, as_of: datetime | None = None) -> bool:
        self.get(fact_id)  # raises on unknown id
        with self._conn.cursor() as cur:
            if as_of is None:
                cur.execute(
                    "SELECT 1 FROM institutional_facts WHERE supersedes_fact_id = %s LIMIT 1",
                    (fact_id,),
                )
            else:
                cur.execute(
                    "SELECT 1 FROM institutional_facts"
                    " WHERE supersedes_fact_id = %s AND retrieved_at <= %s LIMIT 1",
                    (fact_id, as_of),
                )
            return cur.fetchone() is None

    def current_facts_as_of(self, decision_time: datetime) -> list[InstitutionalFact]:
        return self._select_facts(
            "SELECT f.record FROM institutional_facts f"
            " WHERE f.retrieved_at <= %s"
            " AND NOT EXISTS ("
            "   SELECT 1 FROM institutional_facts s"
            "   WHERE s.supersedes_fact_id = f.fact_id AND s.retrieved_at <= %s)"
            " ORDER BY f.fact_id",
            (decision_time, decision_time),
        )

    def validation_status(self, fact_id: str) -> ValidationStatus:
        status = self._latest_event_status("fact_validation_events", fact_id)
        return ValidationStatus(status) if status else ValidationStatus.PENDING

    def freshness_status(self, fact_id: str) -> FreshnessStatus:
        status = self._latest_event_status("fact_freshness_events", fact_id)
        return FreshnessStatus(status) if status else FreshnessStatus.FRESH

    def validation_history(self, fact_id: str) -> list[FactValidationEvent]:
        with self._conn.cursor() as cur:
            cur.execute(
                "SELECT event_id, fact_id, status, reason, occurred_at, recorded_by"
                " FROM fact_validation_events WHERE fact_id = %s"
                " ORDER BY occurred_at ASC, event_seq ASC",
                (fact_id,),
            )
            rows = cur.fetchall()
        return [
            FactValidationEvent(
                event_id=r[0],
                fact_id=r[1],
                status=ValidationStatus(r[2]),
                reason=r[3],
                occurred_at=r[4],
                recorded_by=r[5],
            )
            for r in rows
        ]

    def usable_for_calculation(self, fact_id: str) -> bool:
        fact = self.get(fact_id)
        return fact.usable_for_calculation and (
            self.validation_status(fact_id) is ValidationStatus.VALID
        )

    # ---- internals ----------------------------------------------------------

    def _select_facts(self, sql: str, params: tuple[Any, ...]) -> list[InstitutionalFact]:
        with self._conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
        return [_parse_record(r[0]) for r in rows]

    def _insert_event(self, table: str, event: FactValidationEvent | FactFreshnessEvent) -> None:
        try:
            self._insert_event_inner(table, event)
        except Exception:
            self._conn.rollback()
            raise

    def _insert_event_inner(
        self, table: str, event: FactValidationEvent | FactFreshnessEvent
    ) -> None:
        self.get(event.fact_id)  # raises on unknown fact
        with self._conn.cursor() as cur:
            cur.execute(
                f"INSERT INTO {table}"
                " (event_id, fact_id, status, reason, occurred_at, recorded_by)"
                " VALUES (%s, %s, %s, %s, %s, %s)",
                (
                    event.event_id,
                    event.fact_id,
                    event.status.value,
                    event.reason,
                    event.occurred_at,
                    event.recorded_by,
                ),
            )
        self._conn.commit()

    def _latest_event_status(self, table: str, fact_id: str) -> str | None:
        self.get(fact_id)  # raises on unknown fact
        with self._conn.cursor() as cur:
            # event_seq breaks occurred_at ties by insertion order, matching
            # in-memory append-order semantics deterministically.
            cur.execute(
                f"SELECT status FROM {table}"
                " WHERE fact_id = %s ORDER BY occurred_at DESC, event_seq DESC LIMIT 1",
                (fact_id,),
            )
            row = cur.fetchone()
        return row[0] if row else None

    def _check_chain_acyclic(self, cur: Any, incoming: InstitutionalFact) -> None:
        seen = {incoming.fact_id}
        cursor_id = incoming.supersedes_fact_id
        while cursor_id is not None:
            if cursor_id in seen:
                raise FactStoreError("Revision chain would contain a cycle.")
            seen.add(cursor_id)
            cur.execute(
                "SELECT supersedes_fact_id FROM institutional_facts WHERE fact_id = %s",
                (cursor_id,),
            )
            row = cur.fetchone()
            cursor_id = row[0] if row else None
