"""PostgresReportRepository — persistent append-only report store.

All SQL lives here. Reuses the shared migration runner (advisory-locked,
idempotent); reads re-validate the canonical JSON through the Pydantic model.
"""

from __future__ import annotations

import logging
from typing import Any

from ares.facts.postgres import apply_migrations
from ares.pipeline.output import ResearchReport

from .repository import ReportStoreError, ReportSummary

try:
    import psycopg
except ImportError:  # pragma: no cover - exercised only without the extra
    psycopg = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)


def _parse(raw: Any) -> ResearchReport:
    if isinstance(raw, (str, bytes)):
        return ResearchReport.model_validate_json(raw)
    return ResearchReport.model_validate(raw)


class PostgresReportRepository:
    """Append-only by construction and by database trigger."""

    def __init__(self, dsn: str) -> None:
        if psycopg is None:
            raise RuntimeError(
                "PostgresReportRepository requires psycopg; install 'ares-core[postgres]'."
            )
        self._conn = psycopg.connect(dsn)
        applied = apply_migrations(self._conn)
        if applied:
            logger.info("postgres: applied migrations %s", applied)

    def close(self) -> None:
        self._conn.close()

    def append(self, report: ResearchReport) -> ResearchReport:
        try:
            with self._conn.cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM research_reports WHERE report_id = %s", (report.report_id,)
                )
                if cur.fetchone():
                    raise ReportStoreError(
                        f"report_id {report.report_id!r} already exists (append-only)."
                    )
                cur.execute(
                    "INSERT INTO research_reports"
                    " (report_id, entity_id, data_mode, pipeline_version, generated_at, record)"
                    " VALUES (%s, %s, %s, %s, %s, %s)",
                    (
                        report.report_id,
                        report.entity.entity_id,
                        report.data_mode.value,
                        report.pipeline_version,
                        report.generated_at,
                        report.model_dump_json(),
                    ),
                )
            self._conn.commit()
        except Exception:
            self._conn.rollback()
            raise
        return report

    def get(self, report_id: str) -> ResearchReport:
        with self._conn.cursor() as cur:
            cur.execute("SELECT record FROM research_reports WHERE report_id = %s", (report_id,))
            row = cur.fetchone()
        if row is None:
            raise ReportStoreError(f"Unknown report_id {report_id!r}.")
        return _parse(row[0])

    def list_summaries(self) -> list[ReportSummary]:
        with self._conn.cursor() as cur:
            cur.execute("SELECT record FROM research_reports ORDER BY generated_at DESC")
            rows = cur.fetchall()
        return [ReportSummary.from_report(_parse(r[0])) for r in rows]
