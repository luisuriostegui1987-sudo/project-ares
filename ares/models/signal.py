"""Signal Object — a deterministic measurement/anomaly derived from Facts
(ARES-005 Opportunity Pipeline Sec 7 / ARES-015).

A Signal is *computed*; unlike a Fact it carries no source or knowledge class.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from .base import new_id
from .enums import Direction


class Signal(BaseModel):
    entity_id: str = Field(min_length=1)
    signal_type: str = Field(min_length=1)
    observed_at: datetime
    measured_value: float
    baseline_value: float
    source_fact_ids: list[str] = Field(default_factory=list)
    lookback_window: str | None = None
    anomaly_strength: float | None = Field(default=None, ge=0)
    direction: Direction | None = None
    freshness_status: str = "fresh"
    rule_version: str = "SIGNAL-1.0"
    discovery_cost: float | None = Field(default=None, ge=0)
    signal_id: str = Field(default_factory=lambda: new_id("sig"))
