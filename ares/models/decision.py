"""Decision — a record in the immutable Paper Decision Ledger (ARES-003 Sec 5.11).

Encodes Constitution Sec 4 (human authority) and Sec 6 (deterministic risk) IN
CODE: an APPROVE cannot be constructed without an explicit human approval, and
cannot approve over a FAILED risk result. No AI moves capital — enforced here.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from .base import new_id, require, utcnow
from .enums import InvestmentDecisionType, RiskVerdict, TimeHorizon


@dataclass
class Decision:
    thesis_id: str
    decision: InvestmentDecisionType
    rationale: str
    thesis_version: int = 1
    target_horizon: Optional[TimeHorizon] = None
    reference_price: Optional[float] = None
    paper_position_size: Optional[float] = None
    risk_result: Optional[RiskVerdict] = None
    operator_notes: str = ""
    decided_by: str = "operator"
    human_approved: bool = False
    decision_timestamp: datetime = field(default_factory=utcnow)
    decision_id: str = field(default_factory=lambda: new_id("dec"))

    def __post_init__(self) -> None:
        require(bool(self.thesis_id), "Decision.thesis_id is required")
        require(bool(self.rationale), "Decision.rationale is required")

        if self.decision == InvestmentDecisionType.APPROVE:
            # Constitution Sec 4: only a human may approve capital exposure.
            require(
                self.human_approved is True,
                "APPROVE requires human_approved=True. No AI moves capital "
                "(Constitution Sec 4).",
            )
            # Constitution Sec 6: cannot approve over a failed hard risk rule.
            require(
                self.risk_result != RiskVerdict.FAIL,
                "Cannot APPROVE a thesis whose risk_result is FAIL "
                "(Constitution Sec 6).",
            )
