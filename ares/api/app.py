"""ARES institutional API — FastAPI application factory.

The API is the ONLY entry point for clients: it exposes research runs and
persisted reports, nothing else. Governance holds at the boundary:

- No scoring, risk, decision, portfolio or trading endpoints exist.
- data_mode is explicit per request; a LIVE failure is a clear 502 — the API
  never silently substitutes mock data.
- Reports and facts are append-only; the API offers no mutation of either.
"""

from __future__ import annotations

import base64
import logging
import os
import secrets as py_secrets
from collections.abc import Awaitable, Callable
from importlib import resources
from typing import Any, Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, Response
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
    database: str
    mock_data_warning: str


def create_app(service: ResearchService | None = None) -> FastAPI:
    # Temporary single-user protection (pre-authentication sprint). Credentials
    # come ONLY from the environment; production refuses to start without them.
    ui_user = os.environ.get("ARES_UI_USER", "")
    ui_password = os.environ.get("ARES_UI_PASSWORD", "")
    production = os.environ.get("ARES_ENV", "").strip().lower() == "production"
    if production and not (ui_user and ui_password):
        raise RuntimeError(
            "ARES_ENV=production requires ARES_UI_USER and ARES_UI_PASSWORD; "
            "refusing to start an unprotected public instance."
        )
    auth_enabled = bool(ui_user and ui_password)

    app = FastAPI(
        title="ARES Institutional API",
        version=ares.__version__,
        description=(
            "AI-native investment RESEARCH system. Not a trading bot; paper-only. "
            "A human makes every capital decision. Mock data is always labeled."
        ),
    )
    svc = service if service is not None else ResearchService()

    @app.middleware("http")
    async def _basic_auth(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        # /health stays open for the platform health checker; it carries no
        # secrets. EVERYTHING else (console, research routes, docs, openapi)
        # requires credentials whenever they are configured.
        if not auth_enabled or request.url.path == "/health":
            return await call_next(request)
        header = request.headers.get("authorization", "")
        authorized = False
        if header.startswith("Basic "):
            try:
                decoded = base64.b64decode(header[6:], validate=True).decode("utf-8")
                user, _, password = decoded.partition(":")
                # Constant-time comparison; & (not `and`) evaluates both sides.
                authorized = py_secrets.compare_digest(user, ui_user) & py_secrets.compare_digest(
                    password, ui_password
                )
            except (ValueError, UnicodeDecodeError):
                authorized = False
        if not authorized:
            return Response(
                status_code=401,
                content="Unauthorized",
                headers={"WWW-Authenticate": 'Basic realm="ARES"'},
            )
        return await call_next(request)

    @app.get("/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        """Availability + version + minimal database probe. Never exposes the
        DSN, credentials, hostnames, environment variables or stack traces."""
        try:
            database = svc.reports.ping()
        except Exception:  # noqa: BLE001 - a health probe must degrade, not crash
            logger.warning("health: database ping failed")  # deliberately no details
            database = "error"
        return HealthResponse(
            status="ok" if database != "error" else "degraded",
            version=ares.__version__,
            report_store=type(svc.reports).__name__,
            database=database,
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
