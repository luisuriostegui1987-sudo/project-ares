"""Release version alignment: package == pyproject == OpenAPI (v0.4.0)."""

from __future__ import annotations

import tomllib
from pathlib import Path

import ares
from ares.api import create_app
from ares.reports import InMemoryReportStore
from ares.service import ResearchService

EXPECTED = "0.4.0"


def test_package_version() -> None:
    assert ares.__version__ == EXPECTED


def test_pyproject_version() -> None:
    pyproject = Path(__file__).resolve().parent.parent / "pyproject.toml"
    data = tomllib.loads(pyproject.read_text("utf-8"))
    assert data["project"]["version"] == EXPECTED


def test_openapi_version_follows_package() -> None:
    app = create_app(ResearchService(reports=InMemoryReportStore()))
    assert app.openapi()["info"]["version"] == EXPECTED
