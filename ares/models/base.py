"""Shared base helpers for ARES domain models.

The models use stdlib dataclasses so the first commit runs without external
deps. Per ADR-023 the target stack is Pydantic v2; migration is field-for-field
(each ``@dataclass`` becomes a ``BaseModel`` and each ``_validate`` check becomes
a ``@field_validator`` / ``@model_validator``). See README.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone


class AresValidationError(ValueError):
    """Raised when a model violates an ARES governance rule."""


def new_id(prefix: str) -> str:
    """Generate a stable, prefixed id, e.g. ``fact_3f9a...``."""
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def require(condition: bool, message: str) -> None:
    """Assert an ARES rule, raising :class:`AresValidationError` if violated."""
    if not condition:
        raise AresValidationError(message)


def in_range(value, low: float, high: float) -> bool:
    return value is None or (low <= value <= high)
