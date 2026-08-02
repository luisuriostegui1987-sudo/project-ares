"""FactRepository contract suite — every implementation must behave identically.

Runs against InMemoryFactStore always. When ARES_PG_DSN is set (locally or in
CI's postgres service container), the SAME tests run against
PostgresFactRepository, proving point-in-time behavior is identical.
"""

from __future__ import annotations

import os
import uuid
from collections.abc import Iterator
from datetime import UTC, datetime, timedelta

import pytest
from _helpers import kwargs

from ares.facts import FactRepository, FactStoreError, InMemoryFactStore
from ares.models import FactFreshnessEvent, FactValidationEvent, InstitutionalFact
from ares.models.base import utcnow
from ares.models.vocab import FreshnessStatus, RevisionType, ValidationStatus

T1 = datetime(2026, 6, 1, tzinfo=UTC)
T2 = datetime(2026, 7, 1, tzinfo=UTC)  # decision time
T3 = datetime(2026, 8, 1, tzinfo=UTC)

_PG_DSN = os.environ.get("ARES_PG_DSN")

PARAMS = [
    pytest.param("memory", id="memory"),
    pytest.param(
        "postgres",
        id="postgres",
        marks=pytest.mark.skipif(
            not _PG_DSN, reason="postgres contract tests are opt-in (set ARES_PG_DSN)"
        ),
    ),
]


@pytest.fixture(params=PARAMS)
def repo(request: pytest.FixtureRequest) -> Iterator[FactRepository]:
    if request.param == "memory":
        yield InMemoryFactStore()
        return
    from ares.facts.postgres import PostgresFactRepository

    repository = PostgresFactRepository(_PG_DSN or "")
    yield repository
    repository.close()


def _fact(**overrides: object) -> InstitutionalFact:
    # Unique subject per test invocation: postgres persists across tests,
    # so each test works in its own fact_key/hash namespace.
    unique = f"CIK{uuid.uuid4().hex[:12]}"
    base = kwargs(retrieved_at=T1, subject_scope_id=unique)
    base.update(overrides)
    return InstitutionalFact(**base)


def test_append_and_get_roundtrip(repo: FactRepository) -> None:
    fact = repo.append(_fact())
    assert repo.get(fact.fact_id) == fact  # identity verified by model validators


def test_dedup_is_idempotent(repo: FactRepository) -> None:
    a = _fact()
    b = InstitutionalFact(**{**dict(a), "fact_id": "ifact_" + uuid.uuid4().hex[:12]})
    kept_a = repo.append(a)
    kept_b = repo.append(b)  # same content_hash -> same record
    assert kept_b.fact_id == kept_a.fact_id
    assert len(repo.by_fact_key(a.fact_key)) == 1


def test_same_assertion_from_two_sources_coexists(repo: FactRepository) -> None:
    """Corroboration is never destroyed: the record hash embeds source identity,
    so UNIQUE(content_hash) can only collapse the SAME source record."""
    a = _fact()
    b = InstitutionalFact(
        **{
            **dict(a),
            "fact_id": "ifact_" + uuid.uuid4().hex[:12],
            "source_id": "bloomberg.terminal",
            "source_locator": "bloomberg:NVDA/revenue/fy2025",
            "content_hash": "",  # recomputed: differs because provenance differs
        }
    )
    kept_a, kept_b = repo.append(a), repo.append(b)
    assert kept_a.fact_id != kept_b.fact_id
    assert kept_a.content_hash != kept_b.content_hash
    assert kept_a.fact_key == kept_b.fact_key  # same logical assertion
    stored = {f.fact_id: f for f in repo.by_fact_key(a.fact_key)}
    assert set(stored) == {kept_a.fact_id, kept_b.fact_id}
    assert stored[kept_a.fact_id].source_id == "sec.edgar"
    assert stored[kept_b.fact_id].source_id == "bloomberg.terminal"  # provenance intact


def test_future_retrieved_at_rejected(repo: FactRepository) -> None:
    with pytest.raises(FactStoreError, match="future"):
        repo.append(_fact(retrieved_at=utcnow() + timedelta(days=2)))


def test_point_in_time_hides_later_retrievals(repo: FactRepository) -> None:
    original = repo.append(_fact())
    restated = repo.append(
        InstitutionalFact(
            **{
                **dict(original),
                "fact_id": "ifact_" + uuid.uuid4().hex[:12],
                "value": 131_000_000_000,
                "retrieved_at": T3,
                "revision_type": RevisionType.RESTATEMENT,
                "supersedes_fact_id": original.fact_id,
                "content_hash": "",
            }
        )
    )
    visible_ids = {f.fact_id for f in repo.facts_as_of(T2)}
    assert original.fact_id in visible_ids
    assert restated.fact_id not in visible_ids  # no lookahead bias
    assert repo.is_current(original.fact_id, as_of=T2) is True
    assert repo.is_current(original.fact_id) is False
    assert repo.is_current(restated.fact_id) is True
    current_now = {f.fact_id for f in repo.current_facts_as_of(utcnow())}
    assert restated.fact_id in current_now and original.fact_id not in current_now


def test_restatement_preserves_history(repo: FactRepository) -> None:
    original = repo.append(_fact())
    restated = repo.append(
        InstitutionalFact(
            **{
                **dict(original),
                "fact_id": "ifact_" + uuid.uuid4().hex[:12],
                "value": 999,
                "retrieved_at": T3,
                "revision_type": RevisionType.RESTATEMENT,
                "supersedes_fact_id": original.fact_id,
                "content_hash": "",
            }
        )
    )
    stored = repo.get(original.fact_id)
    assert stored.value == original.value  # untouched
    assert stored.revision_type is RevisionType.ORIGINAL
    assert restated.fact_key == original.fact_key
    assert {f.fact_id for f in repo.by_fact_key(original.fact_key)} == {
        original.fact_id,
        restated.fact_id,
    }


def test_unknown_supersedes_rejected(repo: FactRepository) -> None:
    with pytest.raises(FactStoreError, match="not in the store"):
        repo.append(
            _fact(
                revision_type=RevisionType.CORRECTION,
                supersedes_fact_id="ifact_ghost",
            )
        )


def test_status_events_are_append_only_and_derived(repo: FactRepository) -> None:
    fact = repo.append(_fact())
    assert repo.validation_status(fact.fact_id) is ValidationStatus.PENDING
    assert repo.usable_for_calculation(fact.fact_id) is False
    repo.add_validation_event(
        FactValidationEvent(
            fact_id=fact.fact_id,
            status=ValidationStatus.VALID,
            recorded_by="tests",
            occurred_at=T1,
        )
    )
    repo.add_validation_event(
        FactValidationEvent(
            fact_id=fact.fact_id,
            status=ValidationStatus.CONFLICTED,
            recorded_by="tests",
            occurred_at=T3,
        )
    )
    assert repo.validation_status(fact.fact_id) is ValidationStatus.CONFLICTED
    assert len(repo.validation_history(fact.fact_id)) == 2  # history preserved
    assert repo.usable_for_calculation(fact.fact_id) is False


def test_equal_timestamp_events_break_ties_by_append_order(repo: FactRepository) -> None:
    """Two events with the EXACT same occurred_at: the second appended wins,
    identically in memory (append order) and PostgreSQL (event_seq)."""
    fact = repo.append(_fact())
    for status in (ValidationStatus.VALID, ValidationStatus.CONFLICTED):
        repo.add_validation_event(
            FactValidationEvent(
                fact_id=fact.fact_id, status=status, recorded_by="tests", occurred_at=T1
            )
        )
    assert repo.validation_status(fact.fact_id) is ValidationStatus.CONFLICTED
    history = repo.validation_history(fact.fact_id)
    assert [e.status for e in history] == [ValidationStatus.VALID, ValidationStatus.CONFLICTED]

    for freshness in (FreshnessStatus.STALE, FreshnessStatus.FRESH):
        repo.add_freshness_event(
            FactFreshnessEvent(
                fact_id=fact.fact_id, status=freshness, recorded_by="tests", occurred_at=T1
            )
        )
    assert repo.freshness_status(fact.fact_id) is FreshnessStatus.FRESH  # second appended


def test_event_for_unknown_fact_rejected(repo: FactRepository) -> None:
    with pytest.raises(FactStoreError, match="Unknown fact_id"):
        repo.add_validation_event(
            FactValidationEvent(
                fact_id="ifact_ghost", status=ValidationStatus.VALID, recorded_by="tests"
            )
        )


def test_repository_has_no_mutation_api(repo: FactRepository) -> None:
    for forbidden in ("update", "delete", "remove", "set_validation_status"):
        assert not hasattr(repo, forbidden)


@pytest.mark.skipif(not _PG_DSN, reason="postgres-only: migration lifecycle")
def test_migrations_are_idempotent_and_reversible() -> None:
    """up (already applied) -> no-op; down; up -> re-applied; up -> no-op."""
    from importlib import resources

    import psycopg

    from ares.facts.postgres import apply_migrations

    with psycopg.connect(_PG_DSN or "") as conn:
        assert apply_migrations(conn) == []  # idempotent: already applied
        down_sql = (
            resources.files("ares.facts.migrations")
            .joinpath("0001_institutional_facts_down.sql")
            .read_text("utf-8")
        )
        with conn.cursor() as cur:
            cur.execute(down_sql)  # reversal script drops schema cleanly
        conn.commit()
        assert apply_migrations(conn) == ["0001_institutional_facts.sql"]  # re-applied
        assert apply_migrations(conn) == []  # idempotent again


@pytest.mark.skipif(not _PG_DSN, reason="postgres-only: concurrent initialization")
def test_concurrent_migration_initialization_is_safe() -> None:
    """Two connections racing to initialize a fresh database serialize on the
    advisory lock: exactly one applies migration 0001, the other no-ops."""
    import threading
    from importlib import resources

    import psycopg

    from ares.facts.postgres import apply_migrations

    down_sql = (
        resources.files("ares.facts.migrations")
        .joinpath("0001_institutional_facts_down.sql")
        .read_text("utf-8")
    )
    with psycopg.connect(_PG_DSN or "") as conn:
        with conn.cursor() as cur:
            cur.execute(down_sql)  # fresh database state
        conn.commit()

    results: list[list[str]] = []
    errors: list[Exception] = []

    def initialize() -> None:
        try:
            with psycopg.connect(_PG_DSN or "") as conn:
                results.append(apply_migrations(conn))
        except Exception as exc:  # noqa: BLE001 - the test asserts none occurred
            errors.append(exc)

    threads = [threading.Thread(target=initialize) for _ in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert errors == []
    assert sorted(results, key=len) == [[], ["0001_institutional_facts.sql"]]


@pytest.mark.skipif(not _PG_DSN, reason="postgres-only: JSONB/index integrity constraints")
def test_direct_inconsistent_insert_is_rejected() -> None:
    """A raw SQL insert whose indexed columns diverge from the canonical JSONB
    record must be rejected by the database, column by column."""
    import psycopg

    fact = _fact()
    good = (
        fact.fact_id,
        fact.fact_key,
        fact.content_hash,
        fact.supersedes_fact_id,
        fact.retrieved_at,
        fact.model_dump_json(),
    )
    tampered = [
        ("ifact_drifted", *good[1:]),  # fact_id != record->>'fact_id'
        (good[0], "drifted|key", *good[2:]),  # fact_key drift
        (good[0], good[1], "0" * 64, *good[3:]),  # content_hash drift
        (*good[:3], "ifact_ghost_parent", *good[4:]),  # supersedes drift (non-null vs null)
        (*good[:4], fact.retrieved_at + timedelta(days=1), good[5]),  # retrieved_at drift
    ]
    with psycopg.connect(_PG_DSN or "") as conn:
        for row in tampered:
            with (
                pytest.raises((psycopg.errors.CheckViolation, psycopg.errors.ForeignKeyViolation)),
                conn.cursor() as cur,
            ):
                cur.execute(
                    "INSERT INTO institutional_facts"
                    " (fact_id, fact_key, content_hash, supersedes_fact_id,"
                    "  retrieved_at, record)"
                    " VALUES (%s, %s, %s, %s, %s, %s)",
                    row,
                )
            conn.rollback()


@pytest.mark.skipif(not _PG_DSN, reason="postgres-only: database-level append-only trigger")
def test_postgres_triggers_reject_update_and_delete() -> None:
    import psycopg

    from ares.facts.postgres import PostgresFactRepository

    repository = PostgresFactRepository(_PG_DSN or "")
    try:
        fact = repository.append(_fact())
        conn = repository._conn
        for sql in (
            "UPDATE institutional_facts SET fact_key = 'tampered' WHERE fact_id = %s",
            "DELETE FROM institutional_facts WHERE fact_id = %s",
        ):
            with (
                pytest.raises(psycopg.errors.RaiseException, match="append-only"),
                conn.cursor() as cur,
            ):
                cur.execute(sql, (fact.fact_id,))
            conn.rollback()
    finally:
        repository.close()
