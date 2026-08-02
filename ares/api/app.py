"""ARES institutional API — FastAPI application factory.

The API is the ONLY entry point for clients: it exposes research runs and
persisted reports, nothing else. Governance holds at the boundary:

- No scoring, risk, decision, portfolio or trading endpoints exist.
- data_mode is explicit per request; a LIVE failure is a clear 502 — the API
  never silently substitutes mock data.
- Reports and facts are append-only; the API offers no mutation of either.
"""

from __future__ import annotations

import logging
from importlib import resources
from typing import Any, Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

import ares
from ares.facts import RepositoryConfigError
from ares.pipeline import MOCK_DATA_WARNING, DataMode, ResearchReport
from ares.providers.edgar import EdgarError
from ares.reports import ReportStoreError, ReportSummary
from ares.service import ResearchService

logger = logging.getLogger(__name__)


class AnalyzeRequest(BaseModel):
    ticker: str = Field(min_length=1, max_length=10, description="Ticker symbol, e.g. NVDA.")
    data_mode: Literal["mock", "live"] = Field(
        default="mock",
        description="mock: labeled sample data. live: real SEC EDGAR; fails loudly.",
    )


class HealthResponse(BaseModel):
    status: str
    version: str
    report_store: str
    mock_data_warning: str


def create_app(service: ResearchService | None = None) -> FastAPI:
    app = FastAPI(
        title="ARES Institutional API",
        version=ares.__version__,
        description=(
            "AI-native investment RESEARCH system. Not a trading bot; paper-only. "
            "A human makes every capital decision. Mock data is always labeled."
        ),
    )
    svc = service if service is not None else ResearchService()

    @app.get("/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        return HealthResponse(
            status="ok",
            version=ares.__version__,
            report_store=type(svc.reports).__name__,
            mock_data_warning=MOCK_DATA_WARNING,
        )

    @app.post("/research/analyze", response_model=ResearchReport)
    def analyze(request: AnalyzeRequest) -> ResearchReport:
        mode = DataMode(request.data_mode.upper())
        try:
            return svc.analyze(request.ticker, data_mode=mode)
        except LookupError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except EdgarError as exc:
            raise HTTPException(
                status_code=502,
                detail=f"Live EDGAR retrieval failed: {exc}. "
                "Live mode never falls back to mock data.",
            ) from exc
        except RepositoryConfigError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/research/reports", response_model=list[ReportSummary])
    def list_reports() -> list[ReportSummary]:
        return svc.list_reports()

    @app.get("/research/reports/{report_id}", response_model=ResearchReport)
    def get_report(report_id: str) -> ResearchReport:
        try:
            return svc.get_report(report_id)
        except ReportStoreError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    def index() -> Any:
        html = resources.files("ares.api.static").joinpath("index.html").read_text("utf-8")
        return HTMLResponse(html)

    return app
