"""Shared helpers for ARES domain models (Pydantic v2)."""
from __future__ import annotations

import uuid
from datetime import UTC, datetime


def new_id(prefix: str) -> str:
    """Generate a stable, prefixed id, e.g. ``fact_3f9a...``."""
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def utcnow() -> datetime:
    return datetime.now(UTC)
