"""Append-only institutional fact storage (ARES-FACT-001).

FactRepository is the abstraction business logic depends on; InMemoryFactStore
and PostgresFactRepository are its implementations.

Repository selection is EXPLICIT — persistent execution never silently
becomes ephemeral:

- ARES_FACT_STORE=memory    -> in-memory (tests / local development)
- ARES_FACT_STORE=postgres  -> requires ARES_PG_DSN; missing/invalid DSN is a
                               clear RepositoryConfigError, never a fallback
- unset                     -> postgres when ARES_PG_DSN is configured
                               (configured persistence is never ignored),
                               otherwise in-memory; either way the active
                               repository is logged at startup.
"""

from __future__ import annotations

import logging
import os

from .repository import FactRepository
from .store import FactStoreError, InMemoryFactStore

logger = logging.getLogger(__name__)


class RepositoryConfigError(RuntimeError):
    """Storage selection is misconfigured. Never resolved by a silent fallback."""


def default_repository() -> FactRepository:
    """Resolve the active FactRepository from explicit configuration."""
    mode = os.environ.get("ARES_FACT_STORE", "").strip().lower()
    dsn = os.environ.get("ARES_PG_DSN")
    if mode not in ("", "memory", "postgres"):
        raise RepositoryConfigError(
            f"Unknown ARES_FACT_STORE mode {mode!r}; use 'memory' or 'postgres'."
        )
    if mode == "memory":
        logger.info("fact store: InMemoryFactStore (explicit ARES_FACT_STORE=memory)")
        return InMemoryFactStore()
    if mode == "postgres":
        if not dsn:
            raise RepositoryConfigError(
                "ARES_FACT_STORE=postgres requires ARES_PG_DSN; refusing to fall "
                "back to the in-memory store."
            )
        return _postgres(dsn, "explicit ARES_FACT_STORE=postgres")
    if dsn:
        # Persistence was configured; ignoring it silently is forbidden.
        return _postgres(dsn, "ARES_PG_DSN configured")
    logger.info("fact store: InMemoryFactStore (default; no persistence configured)")
    return InMemoryFactStore()


def _postgres(dsn: str, why: str) -> FactRepository:
    from .postgres import PostgresFactRepository

    try:
        repository = PostgresFactRepository(dsn)
    except Exception as exc:
        raise RepositoryConfigError(f"PostgreSQL fact store unavailable ({why}): {exc}") from exc
    logger.info("fact store: PostgresFactRepository (%s)", why)
    return repository


__all__ = [
    "FactRepository",
    "FactStoreError",
    "InMemoryFactStore",
    "RepositoryConfigError",
    "default_repository",
]
