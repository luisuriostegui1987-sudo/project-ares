"""Append-only institutional fact storage (ARES-FACT-001).

FactRepository is the abstraction business logic depends on; InMemoryFactStore
and PostgresFactRepository are its implementations. default_repository()
selects Postgres when ARES_PG_DSN is set, in-memory otherwise — behavior is
identical either way (proven by the shared contract test suite).
"""

from __future__ import annotations

import os

from .repository import FactRepository
from .store import FactStoreError, InMemoryFactStore


def default_repository() -> FactRepository:
    """Postgres when ARES_PG_DSN is configured; in-memory otherwise."""
    dsn = os.environ.get("ARES_PG_DSN")
    if dsn:
        from .postgres import PostgresFactRepository

        return PostgresFactRepository(dsn)
    return InMemoryFactStore()


__all__ = ["FactRepository", "FactStoreError", "InMemoryFactStore", "default_repository"]
