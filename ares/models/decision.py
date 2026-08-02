"""Decision — a record in the Paper Decision Ledger (Pydantic v2, ARES-003 Sec 5.11).

Encodes Constitution Sec 4 (human authority) and Sec 6 (risk): an APPROVE
requires human_approved=True and cannot approve over a FAILED RiskResult.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from .base import new_id, utcnow
from .enums import InvestmentDecisionType, RiskVerdict, TimeHorizon
from .risk import RiskResult


class Decision(BaseModel):
    thesis_id: str = Field(min_length=1)
    decision: InvestmentDecisionType
    rationale: str = Field(min_length=1)
    thesis_version: int = 1
    target_horizon: TimeHorizon | None = None
    reference_price: float | None = None
    paper_position_size: float | None = Field(default=None, ge=0, le=100)  # approved size
    risk_result: RiskResult | None = None
    operator_notes: str = ""
    decided_by: str = "operator"
    human_approved: bool = False
    decision_timestamp: datetime = Field(default_factory=utcnow)
    decision_id: str = Field(default_factory=lambda: new_id("dec"))

    @model_validator(mode="after")
    def _human_gate(self) -> Decision:
        if self.decision == InvestmentDecisionType.APPROVE:
            if not self.human_approved:
                raise ValueError(
                    "APPROVE requires human_approved=True. No AI moves capital "
                    "(Constitution Sec 4)."
                )
            if self.risk_result is not None and self.risk_result.verdict == RiskVerdict.FAIL:
                raise ValueError("Cannot APPROVE over a FAILED risk_result (Constitution Sec 6).")
        return self
