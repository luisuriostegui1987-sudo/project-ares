"""Explicit storage selection — persistent execution never silently becomes
ephemeral (CTO Gate 2)."""

from __future__ import annotations

import logging
import os

import pytest

from ares.facts import InMemoryFactStore, RepositoryConfigError, default_repository

_PG_DSN = os.environ.get("ARES_PG_DSN")


def test_explicit_memory_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ARES_FACT_STORE", "memory")
    monkeypatch.setenv("ARES_PG_DSN", "postgresql://would-be-ignored/on-purpose")
    assert isinstance(default_repository(), InMemoryFactStore)


def test_postgres_mode_without_dsn_fails_clearly(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ARES_FACT_STORE", "postgres")
    monkeypatch.delenv("ARES_PG_DSN", raising=False)
    with pytest.raises(RepositoryConfigError, match="refusing to fall back"):
        default_repository()


def test_postgres_mode_with_invalid_dsn_fails_clearly(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ARES_FACT_STORE", "postgres")
    monkeypatch.setenv("ARES_PG_DSN", "this-is-not-a-valid-dsn")
    with pytest.raises(RepositoryConfigError, match="unavailable"):
        default_repository()  # clear failure — never a silent memory fallback


def test_unknown_mode_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ARES_FACT_STORE", "sqlite")
    with pytest.raises(RepositoryConfigError, match="Unknown ARES_FACT_STORE"):
        default_repository()


def test_default_without_config_is_memory_and_reported(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    monkeypatch.delenv("ARES_FACT_STORE", raising=False)
    monkeypatch.delenv("ARES_PG_DSN", raising=False)
    with caplog.at_level(logging.INFO, logger="ares.facts"):
        repo = default_repository()
    assert isinstance(repo, InMemoryFactStore)
    assert any("fact store: InMemoryFactStore" in r.message for r in caplog.records)


@pytest.mark.skipif(not _PG_DSN, reason="requires a live PostgreSQL (set ARES_PG_DSN)")
def test_explicit_postgres_mode_with_dsn(monkeypatch: pytest.MonkeyPatch) -> None:
    from ares.facts.postgres import PostgresFactRepository

    monkeypatch.setenv("ARES_FACT_STORE", "postgres")
    repo = default_repository()
    assert isinstance(repo, PostgresFactRepository)
    repo.close()


@pytest.mark.skipif(not _PG_DSN, reason="requires a live PostgreSQL (set ARES_PG_DSN)")
def test_configured_dsn_is_never_silently_ignored(monkeypatch: pytest.MonkeyPatch) -> None:
    from ares.facts.postgres import PostgresFactRepository

    monkeypatch.delenv("ARES_FACT_STORE", raising=False)
    repo = default_repository()  # DSN configured => persistence, not memory
    assert isinstance(repo, PostgresFactRepository)
    repo.close()
