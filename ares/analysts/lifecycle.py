"""Canonical analyst lifecycle enumerations (Sprint 7 Stage 1, D1).

Two independent typed vocabularies, each frozen verbatim with its canonical
source. They are DIFFERENT types describing DIFFERENT entities and must never
be merged, unioned, subclassed into interchangeability or auto-converted:

- :class:`RosterState` — roster-slot lifecycle,
  ARES-ANALYST-ROADMAP-001 §6 (docs/roadmap/ARES-ANALYST-ROADMAP-001.md).
- :class:`ArchitectureState` — analyst/IKP architecture lifecycle,
  ARES-ARCHITECTURE-ANALYST-FRAMEWORK-001 §3
  (docs/architecture/ARES-ARCHITECTURE-ANALYST-FRAMEWORK-001.md).

The Workflow Status of architecture §3.1 is EXCLUDED — NOT AUTHORIZED
(reserved; "no implementation exists or may exist until separately approved").
No type in this package implements it.

Homonyms carry no automatic semantic identity: ``RosterState.DEPRECATED`` and
``ArchitectureState.DEPRECATED`` come from different documents and different
entities. Because these are ``str``-valued enums, *string equality alone
cannot distinguish provenance* — consumers must key on the typed member
(``isinstance``), never on the raw string. The roster↔architecture crosswalk
(with its NO MAPPING — FAIL CLOSED gaps) belongs to D2 and is intentionally
absent here.
"""

from __future__ import annotations

from enum import Enum, unique

ROSTER_STATE_SOURCE = "ARES-ANALYST-ROADMAP-001 §6"
ARCHITECTURE_STATE_SOURCE = "ARES-ARCHITECTURE-ANALYST-FRAMEWORK-001 §3"


@unique
class RosterState(str, Enum):
    """Roster-slot lifecycle state — ARES-ANALYST-ROADMAP-001 §6, verbatim.

    Linear sequence (10) plus non-linear states (5). The set is closed: any
    value outside this vocabulary must fail (never coerce, never default).
    """

    # Linear lifecycle (roadmap §6):
    # TBD → PROPOSED → PLANNED → RESEARCH_AUTHORIZED → RESEARCH_IN_PROGRESS
    #     → IKP_DRAFTED → VALIDATED → APPROVED → IMPLEMENTED → ACTIVE
    TBD = "TBD"
    PROPOSED = "PROPOSED"
    PLANNED = "PLANNED"
    RESEARCH_AUTHORIZED = "RESEARCH_AUTHORIZED"
    RESEARCH_IN_PROGRESS = "RESEARCH_IN_PROGRESS"
    IKP_DRAFTED = "IKP_DRAFTED"
    VALIDATED = "VALIDATED"
    APPROVED = "APPROVED"
    IMPLEMENTED = "IMPLEMENTED"
    ACTIVE = "ACTIVE"
    # Non-linear states (roadmap §6):
    DEFERRED = "DEFERRED"
    REJECTED = "REJECTED"
    SUSPENDED = "SUSPENDED"
    SUPERSEDED = "SUPERSEDED"
    DEPRECATED = "DEPRECATED"


@unique
class ArchitectureState(str, Enum):
    """Analyst architecture lifecycle state — ARES-ARCHITECTURE-ANALYST-FRAMEWORK-001 §3.

    Member names use underscores where the canonical term contains a hyphen;
    the serialized ``value`` preserves the canonical wording exactly
    (e.g. ``CTO-IMPLEMENTATION-REVIEWED``).
    """

    # CANDIDATE → AUTHORIZED (gate 8) → RESEARCHED → PACKAGED
    #   → CTO-IMPLEMENTATION-REVIEWED → CRO-VALIDATED → QUANT-VALIDATED
    #   → PRODUCTION → DEPRECATED   (architecture §3)
    CANDIDATE = "CANDIDATE"
    AUTHORIZED = "AUTHORIZED"
    RESEARCHED = "RESEARCHED"
    PACKAGED = "PACKAGED"
    CTO_IMPLEMENTATION_REVIEWED = "CTO-IMPLEMENTATION-REVIEWED"
    CRO_VALIDATED = "CRO-VALIDATED"
    QUANT_VALIDATED = "QUANT-VALIDATED"
    PRODUCTION = "PRODUCTION"
    DEPRECATED = "DEPRECATED"
