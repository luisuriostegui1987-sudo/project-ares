"""Append-only research report persistence (Sprint 4).

Same explicit selection semantics as the fact store (never a silent
fallback from configured persistence to memory):

- ARES_FACT_STORE=memory    -> in-memory
- ARES_FACT_STORE=postgres  -> requires ARES_PG_DSN (clear failure otherwise)
- unset                     -> postgres when ARES_PG_DSN is configured,
                               otherwise memory; either way logged.
"""

from __future__ import annotations

import logging
import os

from ares.facts import RepositoryConfigError

from .repository import ReportRepository, ReportStoreError, ReportSummary
from .store import InMemoryReportStore

logger = logging.getLogger(__name__)


def default_report_repository() -> ReportRepository:
    """Resolve the active ReportRepository from explicit configuration."""
    mode = os.environ.get("ARES_FACT_STORE", "").strip().lower()
    dsn = os.environ.get("ARES_PG_DSN")
    if mode not in ("", "memory", "postgres"):
        raise RepositoryConfigError(
            f"Unknown ARES_FACT_STORE mode {mode!r}; use 'memory' or 'postgres'."
        )
    if mode == "memory":
        logger.info("report store: InMemoryReportStore (explicit ARES_FACT_STORE=memory)")
        return InMemoryReportStore()
    if mode == "postgres" and not dsn:
        raise RepositoryConfigError(
            "ARES_FACT_STORE=postgres requires ARES_PG_DSN; refusing to fall "
            "back to the in-memory report store."
        )
    if dsn:
        from .postgres import PostgresReportRepository

        try:
            repository = PostgresReportRepository(dsn)
        except Exception as exc:
            raise RepositoryConfigError(f"PostgreSQL report store unavailable: {exc}") from exc
        logger.info("report store: PostgresReportRepository")
        return repository
    logger.info("report store: InMemoryReportStore (default; no persistence configured)")
    return InMemoryReportStore()


__all__ = [
    "InMemoryReportStore",
    "ReportRepository",
    "ReportStoreError",
    "ReportSummary",
    "default_report_repository",
]
