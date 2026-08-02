"""ResearchService: run + persist, append-only artifacts."""

from __future__ import annotations

import pytest

from ares.pipeline import DataMode
from ares.reports import InMemoryReportStore, ReportStoreError
from ares.service import ResearchService


def test_analyze_runs_pipeline_and_persists() -> None:
    service = ResearchService(reports=InMemoryReportStore())
    report = service.analyze("NVDA", data_mode=DataMode.MOCK)
    assert service.get_report(report.report_id) == report
    summaries = service.list_reports()
    assert len(summaries) == 1
    assert summaries[0].ticker == "NVDA"
    assert summaries[0].data_mode is DataMode.MOCK
    assert summaries[0].signal_count == 1


def test_reports_are_append_only() -> None:
    service = ResearchService(reports=InMemoryReportStore())
    report = service.analyze("NVDA")
    with pytest.raises(ReportStoreError, match="append-only"):
        service.reports.append(report)  # same report_id cannot be re-written
    for forbidden in ("update", "delete", "remove"):
        assert not hasattr(service.reports, forbidden)


def test_two_runs_produce_two_distinct_reports() -> None:
    service = ResearchService(reports=InMemoryReportStore())
    first = service.analyze("NVDA")
    second = service.analyze("CRWV")
    assert first.report_id != second.report_id
    assert {s.ticker for s in service.list_reports()} == {"NVDA", "CRWV"}
