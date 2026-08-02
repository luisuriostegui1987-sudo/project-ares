"""Stage 5 — Signals: deterministic measurements computed from Facts.

Input:  Entity + list[Fact].
Output: list[Signal] (domain model).

A Signal is *computed*, never sourced (ARES-005 Sec 7). Rules here are plain
deterministic code (Constitution: risk/scores are code, never LLM judgment),
and they only consume facts where usable_for_calculation is True.
"""

from __future__ import annotations

import logging

from ares.models import Direction, Fact, Signal

from .entity import Entity
from .facts import (
    METRIC_REVENUE_FY_CURRENT,
    METRIC_REVENUE_FY_PRIOR,
    METRIC_REVENUE_TTM_CURRENT,
    METRIC_REVENUE_TTM_PRIOR,
)

logger = logging.getLogger(__name__)

RULE_VERSION = "SIGNAL-1.1"

# Canonical revenue pairs, strongest first: TTM preferred, fiscal-year fallback.
_REVENUE_PAIRS = (
    (METRIC_REVENUE_TTM_CURRENT, METRIC_REVENUE_TTM_PRIOR, "TTM"),
    (METRIC_REVENUE_FY_CURRENT, METRIC_REVENUE_FY_PRIOR, "FY"),
)


def _usable_metric(facts: list[Fact], metric_name: str) -> Fact | None:
    """Return the newest usable fact for a metric, or None."""
    candidates = [f for f in facts if f.metric_name == metric_name and f.usable_for_calculation]
    if not candidates:
        return None
    return max(candidates, key=lambda f: f.as_of_timestamp)


def revenue_growth_signal(entity: Entity, facts: list[Fact]) -> Signal | None:
    """YoY revenue growth (%) from the canonical TTM revenue fact pair.

    Returns None (with a log line) when inputs are missing or unusable —
    a missing signal is a valid outcome, a guessed one is not.
    """
    current = prior = None
    window = ""
    for current_name, prior_name, window in _REVENUE_PAIRS:
        current = _usable_metric(facts, current_name)
        prior = _usable_metric(facts, prior_name)
        if current is not None and prior is not None:
            break
    if current is None or prior is None:
        logger.info(
            "signals: revenue growth skipped for %s (missing usable facts)", entity.entity_id
        )
        return None
    if not isinstance(current.value, (int, float)) or not isinstance(prior.value, (int, float)):
        logger.warning("signals: revenue facts for %s are non-numeric", entity.entity_id)
        return None
    if prior.value == 0:
        logger.warning("signals: prior revenue is zero for %s", entity.entity_id)
        return None
    growth_pct = (float(current.value) - float(prior.value)) / float(prior.value) * 100.0
    direction = (
        Direction.LONG
        if growth_pct > 0
        else (Direction.SHORT if growth_pct < 0 else Direction.NEUTRAL)
    )
    return Signal(
        entity_id=entity.entity_id,
        signal_type="revenue_growth_yoy_pct",
        observed_at=current.as_of_timestamp,
        measured_value=round(growth_pct, 2),
        baseline_value=0.0,
        lookback_window=window,
        source_fact_ids=[current.fact_id, prior.fact_id],
        direction=direction,
        rule_version=RULE_VERSION,
    )


def derive_signals(entity: Entity, facts: list[Fact]) -> list[Signal]:
    """Run every signal rule; validate fact ownership first."""
    foreign = [f.fact_id for f in facts if f.entity_id != entity.entity_id]
    if foreign:
        raise ValueError(f"Facts {foreign} do not belong to entity {entity.entity_id!r}.")
    signals = [s for s in (revenue_growth_signal(entity, facts),) if s is not None]
    logger.info("signals: %d derived for %s", len(signals), entity.entity_id)
    return signals
