"""ReportRepository contract — memory always, PostgreSQL when ARES_PG_DSN set."""

from __future__ import annotations

import os
from collections.abc import Iterator

import pytest

from ares.pipeline import ResearchPipeline
from ares.pipeline.output import ResearchReport
from ares.reports import InMemoryReportStore, ReportRepository, ReportStoreError

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
def repo(request: pytest.FixtureRequest) -> Iterator[ReportRepository]:
    if request.param == "memory":
        yield InMemoryReportStore()
        return
    from ares.reports.postgres import PostgresReportRepository

    repository = PostgresReportRepository(_PG_DSN or "")
    yield repository
    repository.close()


def _report() -> ResearchReport:
    return ResearchPipeline().run("NVDA")  # unique report_id per run


def test_append_get_roundtrip(repo: ReportRepository) -> None:
    report = repo.append(_report())
    assert repo.get(report.report_id) == report  # revalidated through the model


def test_duplicate_report_id_rejected(repo: ReportRepository) -> None:
    report = repo.append(_report())
    with pytest.raises(ReportStoreError, match="append-only"):
        repo.append(report)


def test_unknown_report_id_raises(repo: ReportRepository) -> None:
    with pytest.raises(ReportStoreError, match="Unknown report_id"):
        repo.get("report_ghost")


def test_summaries_list_newest_first(repo: ReportRepository) -> None:
    first = repo.append(_report())
    second = repo.append(_report())
    summaries = repo.list_summaries()
    ids = [s.report_id for s in summaries]
    assert ids.index(second.report_id) < ids.index(first.report_id)
    mine = next(s for s in summaries if s.report_id == first.report_id)
    assert mine.ticker == "NVDA" and mine.fact_count == 3


def test_repository_has_no_mutation_api(repo: ReportRepository) -> None:
    for forbidden in ("update", "delete", "remove"):
        assert not hasattr(repo, forbidden)


@pytest.mark.skipif(not _PG_DSN, reason="postgres-only: database-level append-only trigger")
def test_postgres_report_trigger_rejects_update_and_delete() -> None:
    import psycopg

    from ares.reports.postgres import PostgresReportRepository

    repository = PostgresReportRepository(_PG_DSN or "")
    try:
        report = repository.append(_report())
        conn = repository._conn
        for sql in (
            "UPDATE research_reports SET entity_id = 'tampered' WHERE report_id = %s",
            "DELETE FROM research_reports WHERE report_id = %s",
        ):
            with (
                pytest.raises(psycopg.errors.RaiseException, match="append-only"),
                conn.cursor() as cur,
            ):
                cur.execute(sql, (report.report_id,))
            conn.rollback()
    finally:
        repository.close()
