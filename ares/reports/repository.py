"""ReportRepository — storage abstraction for persisted ResearchReports.

Reports are append-only research artifacts: they are stored exactly as
produced (canonical JSON), never mutated, never deleted. Dependency
direction: models <- pipeline <- reports <- service <- api.
"""

from __future__ import annotations

from datetime import datetime
from typing import Protocol, runtime_checkable

from pydantic import BaseModel

from ares.pipeline.output import DataMode, ResearchReport


class ReportStoreError(ValueError):
    """Raised when an operation would violate report-store invariants."""


class ReportSummary(BaseModel):
    """Lightweight listing row; the full report stays canonical."""

    report_id: str
    entity_id: str
    entity_name: str
    ticker: str
    data_mode: DataMode
    pipeline_version: str
    generated_at: datetime
    fact_count: int
    signal_count: int
    claim_count: int

    @classmethod
    def from_report(cls, report: ResearchReport) -> ReportSummary:
        return cls(
            report_id=report.report_id,
            entity_id=report.entity.entity_id,
            entity_name=report.entity.name,
            ticker=report.entity.ticker,
            data_mode=report.data_mode,
            pipeline_version=report.pipeline_version,
            generated_at=report.generated_at,
            fact_count=len(report.facts),
            signal_count=len(report.signals),
            claim_count=len(report.evidence.claims),
        )


@runtime_checkable
class ReportRepository(Protocol):
    """Append-only research report storage."""

    def append(self, report: ResearchReport) -> ResearchReport: ...

    def get(self, report_id: str) -> ResearchReport: ...

    def list_summaries(self) -> list[ReportSummary]: ...
