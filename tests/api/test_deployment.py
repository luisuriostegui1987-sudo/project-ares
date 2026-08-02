"""Deployment hardening: production gate, Basic Auth, health probe,
migration runner, Blueprint secret hygiene."""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from ares.api import create_app
from ares.reports import InMemoryReportStore
from ares.service import ResearchService

_PG_DSN = os.environ.get("ARES_PG_DSN")

USER, PASSWORD = "luis", "test-secret-credential"


def _service() -> ResearchService:
    return ResearchService(reports=InMemoryReportStore())


@pytest.fixture()
def auth_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("ARES_UI_USER", USER)
    monkeypatch.setenv("ARES_UI_PASSWORD", PASSWORD)
    return TestClient(create_app(_service()))


def test_production_startup_fails_without_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ARES_ENV", "production")
    monkeypatch.delenv("ARES_UI_USER", raising=False)
    monkeypatch.delenv("ARES_UI_PASSWORD", raising=False)
    with pytest.raises(RuntimeError, match="refusing to start an unprotected"):
        create_app(_service())


def test_production_starts_with_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ARES_ENV", "production")
    monkeypatch.setenv("ARES_UI_USER", USER)
    monkeypatch.setenv("ARES_UI_PASSWORD", PASSWORD)
    assert create_app(_service()) is not None


def test_unauthenticated_console_is_401(auth_client: TestClient) -> None:
    response = auth_client.get("/")
    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"].startswith("Basic")
    assert PASSWORD not in response.text


@pytest.mark.parametrize(
    "path",
    ["/research/reports", "/research/reports/report_x", "/docs", "/redoc", "/openapi.json"],
)
def test_unauthenticated_routes_are_401(auth_client: TestClient, path: str) -> None:
    assert auth_client.get(path).status_code == 401


def test_unauthenticated_analyze_is_401(auth_client: TestClient) -> None:
    assert auth_client.post("/research/analyze", json={"ticker": "NVDA"}).status_code == 401


def test_invalid_credentials_are_401(auth_client: TestClient) -> None:
    assert auth_client.get("/", auth=(USER, "wrong-password")).status_code == 401
    assert auth_client.get("/", auth=("mallory", PASSWORD)).status_code == 401


def test_valid_credentials_allow_access(auth_client: TestClient) -> None:
    assert auth_client.get("/", auth=(USER, PASSWORD)).status_code == 200
    assert auth_client.get("/research/reports", auth=(USER, PASSWORD)).status_code == 200


def test_health_open_without_auth_and_probes_database(auth_client: TestClient) -> None:
    response = auth_client.get("/health")  # no credentials on purpose
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["database"] == "memory"


def test_health_exposes_no_credentials(auth_client: TestClient) -> None:
    response = auth_client.get("/health")
    text = response.text
    assert set(response.json().keys()) == {
        "status",
        "version",
        "report_store",
        "database",
        "mock_data_warning",
    }
    for forbidden in ("postgres://", "postgresql://", PASSWORD, "ARES_PG_DSN", "@"):
        assert forbidden not in text


@pytest.mark.skipif(not _PG_DSN, reason="requires live PostgreSQL (set ARES_PG_DSN)")
def test_health_database_probe_against_real_postgres() -> None:
    from ares.reports.postgres import PostgresReportRepository

    repository = PostgresReportRepository(_PG_DSN or "")
    try:
        client = TestClient(create_app(ResearchService(reports=repository)))
        body = client.get("/health").json()
        assert body["database"] == "postgres-ok"
        assert "@" not in body["database"]
    finally:
        repository.close()


def test_migrate_command_fails_clearly_without_dsn(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    from ares.facts.migrate import main

    monkeypatch.delenv("ARES_PG_DSN", raising=False)
    assert main() == 1
    assert "refusing to guess" in capsys.readouterr().err


@pytest.mark.skipif(not _PG_DSN, reason="requires live PostgreSQL (set ARES_PG_DSN)")
def test_migrate_command_is_idempotent_and_silent_about_dsn(
    capsys: pytest.CaptureFixture[str],
) -> None:
    from ares.facts.migrate import main

    assert main() == 0
    assert main() == 0  # idempotent: second run is a no-op
    output = capsys.readouterr()
    combined = output.out + output.err
    assert (_PG_DSN or "-") not in combined  # the DSN is never printed
    assert "migrations" in combined


def _blueprint_text() -> str:
    return (Path(__file__).resolve().parents[2] / "render.yaml").read_text("utf-8")


def test_render_blueprint_contains_no_secrets() -> None:
    text = _blueprint_text()
    assert text.count("sync: false") == 3  # SEC UA + UI user + UI password
    assert "fromDatabase" in text  # DSN injected, never written
    assert "healthCheckPath: /health" in text
    assert "preDeployCommand: python -m ares.facts.migrate" in text
    assert "--host 0.0.0.0" in text and "$PORT" in text
    assert "ARES_ENV" in text and "production" in text
    for forbidden in ("postgres://", "postgresql://", "password:", "secret:"):
        assert forbidden not in text


def test_render_blueprint_pins_python_3128_explicitly() -> None:
    """A real PYTHON_VERSION envVar — not a comment or descriptive field."""
    text = _blueprint_text()
    assert "- key: PYTHON_VERSION" in text
    assert 'value: "3.12.8"' in text


def test_render_blueprint_database_is_not_publicly_reachable() -> None:
    text = _blueprint_text()
    assert "ipAllowList: []" in text  # empty allow list: no public access
    # The app connects over the private network via the internal string.
    assert "property: connectionString" in text


def test_render_blueprint_service_and_database_share_region() -> None:
    text = _blueprint_text()
    assert text.count("region: oregon") == 2  # web service AND database
