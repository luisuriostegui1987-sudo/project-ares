"""Stage 7 — Structured Research Output: the pipeline's single artifact.

Input:  every prior stage's output.
Output: ResearchReport — validated, serializable, auditable.

The report validator re-checks cross-stage integrity: every claim and signal
must cite fact_ids that are actually present in the report.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, model_validator

from ares.models import Event, Evidence, Fact, KnowledgeClass, Signal
from ares.models.base import new_id, utcnow

from .context import EntityContext
from .entity import Entity

PIPELINE_VERSION = "SLICE-1.0"

MOCK_DATA_WARNING = "WARNING: This report uses mock data and is not investment research."


class DataMode(str, Enum):
    """Provenance of the data behind a report."""

    MOCK = "MOCK"
    LIVE = "LIVE"


class ResearchReport(BaseModel):
    """Structured output of one research pipeline run (no Risk/Decision in Sprint 1)."""

    entity: Entity
    context: EntityContext
    events: list[Event] = Field(default_factory=list)
    facts: list[Fact] = Field(default_factory=list)
    evidence: Evidence
    signals: list[Signal] = Field(default_factory=list)
    data_mode: DataMode = DataMode.MOCK
    pipeline_version: str = PIPELINE_VERSION
    generated_at: datetime = Field(default_factory=utcnow)
    report_id: str = Field(default_factory=lambda: new_id("report"))

    @model_validator(mode="after")
    def _cross_stage_integrity(self) -> ResearchReport:
        eid = self.entity.entity_id
        sections: list[tuple[str, list[str]]] = [
            ("context", [self.context.entity_id]),
            ("events", [e.entity_id for e in self.events]),
            ("facts", [f.entity_id for f in self.facts]),
            ("signals", [s.entity_id for s in self.signals]),
        ]
        for name, ids in sections:
            if any(i != eid for i in ids):
                raise ValueError(f"Report section {name!r} contains foreign entity_ids.")
        known = {f.fact_id for f in self.facts}
        for claim in self.evidence.claims:
            missing = set(claim.supporting_fact_ids) - known
            if missing:
                raise ValueError(f"Claim {claim.claim_id} cites unknown facts: {sorted(missing)}.")
        for signal in self.signals:
            missing = set(signal.source_fact_ids) - known
            if missing:
                raise ValueError(
                    f"Signal {signal.signal_id} cites unknown facts: {sorted(missing)}."
                )
        # Structural governance rule: mock data can never carry Verified Fact.
        if self.data_mode is DataMode.MOCK:
            verified = [
                f.fact_id for f in self.facts if f.knowledge_class is KnowledgeClass.VERIFIED_FACT
            ]
            if verified:
                raise ValueError(f"MOCK report cannot contain Verified Fact facts: {verified}.")
        return self


def render_text(report: ResearchReport) -> str:
    """Human-readable summary for the CLI. JSON stays the canonical format."""
    e = report.entity
    lines = [
        *([MOCK_DATA_WARNING] if report.data_mode is DataMode.MOCK else []),
        f"ARES research report — {e.name} ({e.ticker})",
        f"  data_mode: {report.data_mode.value}",
        f"  report_id: {report.report_id}   pipeline: {report.pipeline_version}",
        f"  sector: {e.sector or '-'} / {e.industry or '-'}",
        f"  context: {report.context.business_summary}",
        f"  events ({len(report.events)}):",
        *[
            f"    - [{ev.event_type.value}] {ev.title} @ {ev.occurs_at.date().isoformat()}"
            + ("  [CATALYST]" if ev.is_catalyst else "")
            for ev in report.events
        ],
        f"  facts ({len(report.facts)}):",
        *[
            f"    - {f.metric_name} = {f.value} {f.unit or ''} [{f.knowledge_class.value}]"
            for f in report.facts
        ],
        (f"  evidence: {report.evidence.summary} (overall: {report.evidence.overall_class.value})"),
        f"  signals ({len(report.signals)}):",
        *[
            f"    - {s.signal_type} = {s.measured_value} (baseline {s.baseline_value}, "
            f"{s.direction.value if s.direction else 'n/a'}, rule {s.rule_version})"
            for s in report.signals
        ],
    ]
    return "\n".join(lines)
