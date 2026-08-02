"""Stage 6 — Evidence: sourced Facts marshaled into auditable Claims.

Input:  Entity + list[Fact].
Output: Evidence (domain model) whose every claim cites real fact_ids.

Runs BEFORE Signals in the approved pipeline order, so claims are built
strictly from sourced facts via deterministic templates — no free-form
assertions, no computed values. Knowledge class is inherited from the cited
fact, never upgraded (RULE 17: never launder opinion into fact).
"""

from __future__ import annotations

import logging

from ares.models import Claim, Evidence, Fact

from .entity import Entity

logger = logging.getLogger(__name__)


def _fact_claim(entity: Entity, fact: Fact) -> Claim:
    """Deterministic restatement of one sourced fact as an auditable claim."""
    unit = f" {fact.unit}" if fact.unit and fact.unit != "%" else (fact.unit or "")
    value = f"{fact.value:,}" if isinstance(fact.value, (int, float)) else str(fact.value)
    return Claim(
        statement=(
            f"{entity.ticker} {fact.metric_name} = {value}{unit} "
            f"as of {fact.as_of_timestamp.date().isoformat()} (source: {fact.source_name})."
        ),
        knowledge_class=fact.knowledge_class,
        supporting_fact_ids=[fact.fact_id],
        reasoning_summary="Direct restatement of a sourced fact.",
    )


def derive_evidence(entity: Entity, facts: list[Fact]) -> Evidence:
    """Build Evidence from facts; unusable facts become unresolved questions, not claims."""
    foreign = [f.fact_id for f in facts if f.entity_id != entity.entity_id]
    if foreign:
        raise ValueError(f"Facts {foreign} do not belong to entity {entity.entity_id!r}.")

    usable = [f for f in facts if f.usable_for_calculation]
    skipped = [f for f in facts if not f.usable_for_calculation]

    claims = [_fact_claim(entity, f) for f in usable]
    if skipped and claims:
        claims[0].unresolved_questions.extend(
            f"Fact {f.fact_id} ({f.metric_name}) is {f.knowledge_class.value}; "
            "not usable as evidence for calculation."
            for f in skipped
        )

    evidence = Evidence(
        subject=f"{entity.ticker} research (Sprint-1 slice)",
        claims=claims,
        supporting_fact_ids=sorted({fid for c in claims for fid in c.supporting_fact_ids}),
        summary=f"{len(claims)} deterministic claims over {len(usable)} usable facts "
        f"({len(skipped)} excluded).",
    )
    logger.info(
        "evidence: %d claims for %s (overall class: %s)",
        len(claims),
        entity.entity_id,
        evidence.overall_class.value,
    )
    return evidence
