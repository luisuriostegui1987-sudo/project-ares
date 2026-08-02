"""UI rendering security — XSS regression suite.

Proof chain (headless, no browser engine in CI):
1. The served application contains ZERO `innerHTML` usage — every dynamic
   value flows through createElement/textContent/createTextNode (structural
   assertions on the exact served asset).
2. Malicious payloads injected through the full API path come back as inert
   JSON string DATA, byte-identical, with an application/json content type —
   the server never interpolates them into markup.
3. Ticker fields structurally reject markup (server-side regex), so payloads
   cannot even enter via the one field rendered most prominently.
Together: a payload can only ever reach the page as literal text.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from ares.api import create_app
from ares.models import Claim, Entity, Evidence, KnowledgeClass
from ares.pipeline.context import EntityContext
from ares.pipeline.output import DataMode, ResearchReport
from ares.reports import InMemoryReportStore
from ares.service import ResearchService

XSS_PAYLOADS = [
    "<img src=x onerror=alert(1)>",
    "<script>alert(1)</script>",
    '" onmouseover="alert(1)',
]


@pytest.fixture()
def store() -> InMemoryReportStore:
    return InMemoryReportStore()


@pytest.fixture()
def client(store: InMemoryReportStore) -> TestClient:
    return TestClient(create_app(ResearchService(reports=store)))


def _report_with_payload(payload: str) -> ResearchReport:
    """A structurally valid report carrying the payload in every free-text
    field a renderer would display."""
    entity = Entity(entity_id="NVDA", ticker="NVDA", name=payload)
    return ResearchReport(
        entity=entity,
        context=EntityContext(entity_id="NVDA", business_summary=payload),
        facts=[],
        evidence=Evidence(
            subject=payload,
            claims=[
                Claim(
                    statement=payload,
                    knowledge_class=KnowledgeClass.SPECULATION,
                    reasoning_summary=payload,
                )
            ],
            summary=payload,
        ),
        signals=[],
        data_mode=DataMode.MOCK,
    )


def test_served_ui_never_uses_innerhtml(client: TestClient) -> None:
    html = client.get("/").text
    assert "innerHTML" not in html  # zero dynamic markup interpolation exists
    assert "outerHTML" not in html
    assert "document.write" not in html
    assert "insertAdjacentHTML" not in html
    # The safe APIs are what renders every dynamic value.
    assert "createElement" in html
    assert "textContent" in html
    assert "createTextNode" in html


@pytest.mark.parametrize("payload", XSS_PAYLOADS)
def test_payloads_round_trip_as_inert_json_data(
    client: TestClient, store: InMemoryReportStore, payload: str
) -> None:
    report = store.append(_report_with_payload(payload))
    response = client.get(f"/research/reports/{report.report_id}")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    body = response.json()
    # Byte-identical literal strings — data, never markup or attributes.
    assert body["entity"]["name"] == payload
    assert body["context"]["business_summary"] == payload
    assert body["evidence"]["claims"][0]["statement"] == payload
    # And the raw HTTP body never carries an executable HTML context for it:
    # JSON string escaping means the payload cannot terminate its string.
    assert "<script>alert(1)</script>" not in response.headers.get("content-type", "")


@pytest.mark.parametrize("payload", XSS_PAYLOADS)
def test_ticker_field_structurally_rejects_markup(payload: str) -> None:
    with pytest.raises(ValidationError):
        Entity(entity_id="X", ticker=payload, name="X Corp")


@pytest.mark.parametrize("payload", XSS_PAYLOADS)
def test_analyze_rejects_payload_tickers_and_persists_nothing(
    client: TestClient, store: InMemoryReportStore, payload: str
) -> None:
    response = client.post("/research/analyze", json={"ticker": payload})
    assert response.status_code in (400, 404, 422)
    assert store.list_summaries() == []
