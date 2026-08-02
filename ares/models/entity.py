"""Entity — a resolved, analyzable listed company (ARES-015).

The canonical Entity definition. The research pipeline resolves tickers into
this model; every downstream object keys on its entity_id.
"""

from __future__ import annotations

import re

from pydantic import BaseModel, Field, field_validator

TICKER_RE = re.compile(r"^[A-Z][A-Z0-9.\-]{0,9}$")


class Entity(BaseModel):
    entity_id: str = Field(min_length=1, description="Canonical id; v1 uses the ticker itself.")
    ticker: str
    name: str = Field(min_length=1)
    exchange: str | None = None
    sector: str | None = None
    industry: str | None = None

    @field_validator("ticker")
    @classmethod
    def _ticker_format(cls, v: str) -> str:
        if not TICKER_RE.match(v):
            raise ValueError(f"Invalid ticker format: {v!r} (expected e.g. 'NVDA', 'BRK.B').")
        return v
