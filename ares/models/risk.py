"""RiskResult — output of the deterministic risk engine (ARES-RISK-001 Sec 16).

Replaces the bare RiskVerdict on Thesis/Decision. Recommended size lives here;
approved size lives on Decision; actual size lives on Position.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from .base import new_id
from .enums import RiskVerdict


class RiskResult(BaseModel):
    verdict: RiskVerdict
    recommended_paper_size: float = Field(ge=0, le=100)  # % of paper portfolio
    triggered_rules: list[str] = Field(default_factory=list)
    required_overrides: list[str] = Field(default_factory=list)
    risk_result_id: str = Field(default_factory=lambda: new_id("risk"))
