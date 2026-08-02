"""ResearchService — the single business-logic entry point for research runs.

Every client (API, and any future surface) goes through this service; it runs
the approved pipeline and persists the resulting ResearchReport append-only.
No scoring, no risk, no decisions — research only (Constitution: humans make
every capital decision).
"""

from __future__ import annotations

import logging

from ares.pipeline import DataMode, ResearchPipeline, ResearchReport
from ares.reports import ReportRepository, ReportSummary, default_report_repository

logger = logging.getLogger(__name__)


class ResearchService:
    """Run research and persist the artifact. Reports are never mutated."""

    def __init__(self, reports: ReportRepository | None = None) -> None:
        self.reports = reports if reports is not None else default_report_repository()

    def analyze(self, ticker: str, data_mode: DataMode = DataMode.MOCK) -> ResearchReport:
        """Run the pipeline in the requested mode and persist the report.

        LIVE failures propagate — a live run never silently degrades to mock
        (that guarantee lives in the pipeline; the service adds nothing that
        could weaken it).
        """
        report = ResearchPipeline(data_mode=data_mode).run(ticker)
        self.reports.append(report)
        logger.info(
            "service: stored report %s for %s (mode=%s)",
            report.report_id,
            report.entity.entity_id,
            report.data_mode.value,
        )
        return report

    def get_report(self, report_id: str) -> ResearchReport:
        return self.reports.get(report_id)

    def list_reports(self) -> list[ReportSummary]:
        return self.reports.list_summaries()
