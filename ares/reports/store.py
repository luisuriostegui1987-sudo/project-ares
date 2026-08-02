"""In-memory append-only report store (tests / local development)."""

from __future__ import annotations

from ares.pipeline.output import ResearchReport

from .repository import ReportStoreError, ReportSummary


class InMemoryReportStore:
    """Append-only: no update or delete operation exists on this class."""

    def __init__(self) -> None:
        self._reports: dict[str, ResearchReport] = {}

    def append(self, report: ResearchReport) -> ResearchReport:
        if report.report_id in self._reports:
            raise ReportStoreError(f"report_id {report.report_id!r} already exists (append-only).")
        self._reports[report.report_id] = report
        return report

    def get(self, report_id: str) -> ResearchReport:
        report = self._reports.get(report_id)
        if report is None:
            raise ReportStoreError(f"Unknown report_id {report_id!r}.")
        return report

    def list_summaries(self) -> list[ReportSummary]:
        summaries = [ReportSummary.from_report(r) for r in self._reports.values()]
        return sorted(summaries, key=lambda s: s.generated_at, reverse=True)
