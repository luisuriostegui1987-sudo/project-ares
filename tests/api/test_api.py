"""ARES institutional API tests (mock mode; live failure path monkeypatched)."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from ares.api import create_app
from ares.pipeline import MOCK_DATA_WARNING
from ares.reports import InMemoryReportStore
from ares.service import ResearchService


@pytest.fixture()
def client() -> TestClient:
    service = ResearchService(reports=InMemoryReportStore())
    return TestClient(create_app(service))


def test_health_reports_active_stores(client: TestClient) -> None:
    body = client.get("/health").json()
    assert body["status"] == "ok"
    assert body["report_store"] == "InMemoryReportStore"
    assert body["mock_data_warning"] == MOCK_DATA_WARNING


def test_analyze_mock_returns_labeled_report(client: TestClient) -> None:
    response = client.post("/research/analyze", json={"ticker": "NVDA", "data_mode": "mock"})
    assert response.status_code == 200
    report = response.json()
    assert report["data_mode"] == "MOCK"
    assert report["entity"]["ticker"] == "NVDA"
    assert report["signals"][0]["signal_type"] == "revenue_growth_yoy_pct"


def test_analyze_persists_and_report_is_retrievable(client: TestClient) -> None:
    report = client.post("/research/analyze", json={"ticker": "NVDA"}).json()
    listed = client.get("/research/reports").json()
    assert [row["report_id"] for row in listed] == [report["report_id"]]
    assert listed[0]["data_mode"] == "MOCK"
    fetched = client.get(f"/research/reports/{report['report_id']}")
    assert fetched.status_code == 200
    assert fetched.json() == report


def test_unknown_ticker_is_404(client: TestClient) -> None:
    response = client.post("/research/analyze", json={"ticker": "ZZZZ"})
    assert response.status_code == 404
    assert "Unknown entity" in response.json()["detail"]


def test_invalid_data_mode_is_422(client: TestClient) -> None:
    response = client.post("/research/analyze", json={"ticker": "NVDA", "data_mode": "guess"})
    assert response.status_code == 422


def test_unknown_report_id_is_404(client: TestClient) -> None:
    assert client.get("/research/reports/report_ghost").status_code == 404


def test_live_failure_is_502_and_never_falls_back(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    from ares.providers import edgar

    def refuse(self: edgar.EdgarClient, url: str) -> None:
        raise edgar.EdgarError("simulated SEC outage")

    monkeypatch.setattr(edgar.EdgarClient, "_get_json", refuse)
    response = client.post("/research/analyze", json={"ticker": "NVDA", "data_mode": "live"})
    assert response.status_code == 502
    assert "never falls back to mock data" in response.json()["detail"]
    assert client.get("/research/reports").json() == []  # nothing persisted


def test_ui_is_served_and_self_contained(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    html = response.text
    assert "ARES" in html and "/research/analyze" in html
    assert "http://" not in html and "https://" not in html  # no external assets
    assert "a human makes every capital decision" in html


def test_api_exposes_no_mutation_endpoints() -> None:
    app = create_app(ResearchService(reports=InMemoryReportStore()))
    methods = {m for route in app.routes for m in getattr(route, "methods", set())}
    assert "DELETE" not in methods and "PUT" not in methods and "PATCH" not in methods
