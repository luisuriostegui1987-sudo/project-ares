"""WU-1 evidence contribution for D1 (Sprint 7 Stage 1).

Contributes the WU-1 portion of T-1R (canonical values + §3.1 exclusion),
T-8 (unknown values fail closed) and T-9 (canonical serialization). The full
Stage 1 versions of those tests depend on later WUs and are NOT claimed
complete here.
"""

from __future__ import annotations

import inspect
import json

import pytest

import ares.analysts as analysts_pkg
from ares.analysts import lifecycle
from ares.analysts.lifecycle import (
    ARCHITECTURE_STATE_SOURCE,
    ROSTER_STATE_SOURCE,
    ArchitectureState,
    RosterState,
)

# Verbatim from ARES-ANALYST-ROADMAP-001 §6 (linear sequence, then the
# non-linear states) — the citation IS the expectation.
CANONICAL_ROSTER_VALUES = [
    "TBD",
    "PROPOSED",
    "PLANNED",
    "RESEARCH_AUTHORIZED",
    "RESEARCH_IN_PROGRESS",
    "IKP_DRAFTED",
    "VALIDATED",
    "APPROVED",
    "IMPLEMENTED",
    "ACTIVE",
    "DEFERRED",
    "REJECTED",
    "SUSPENDED",
    "SUPERSEDED",
    "DEPRECATED",
]

# Verbatim from ARES-ARCHITECTURE-ANALYST-FRAMEWORK-001 §3 (canonical
# hyphenated wording preserved in the serialized values).
CANONICAL_ARCHITECTURE_VALUES = [
    "CANDIDATE",
    "AUTHORIZED",
    "RESEARCHED",
    "PACKAGED",
    "CTO-IMPLEMENTATION-REVIEWED",
    "CRO-VALIDATED",
    "QUANT-VALIDATED",
    "PRODUCTION",
    "DEPRECATED",
]

# Workflow Status tokens whose provenance is architecture §3.1 (EXCLUDED —
# NOT AUTHORIZED). Homonyms that §3.1 shares with other documents (APPROVED,
# PRODUCTION, SUPERSEDED, DEPRECATED) are legitimate here ONLY under their
# roster-§6 / architecture-§3 provenance.
FORBIDDEN_31_ONLY_TOKENS = [
    "REQUESTED",
    "RESEARCHING",
    "UNDER_REVIEW",
    "CRO_REVIEW",
    "QUANT_REVIEW",
    "REVISION_REQUIRED",
]


class TestRosterState:
    def test_exactly_15_values_verbatim_in_order(self) -> None:
        assert [m.value for m in RosterState] == CANONICAL_ROSTER_VALUES
        assert len(RosterState) == 15

    def test_provenance_declared(self) -> None:
        assert ROSTER_STATE_SOURCE == "ARES-ANALYST-ROADMAP-001 §6"
        assert "ARES-ANALYST-ROADMAP-001 §6" in (RosterState.__doc__ or "")


class TestArchitectureState:
    def test_exactly_9_values_verbatim_in_order(self) -> None:
        assert [m.value for m in ArchitectureState] == CANONICAL_ARCHITECTURE_VALUES
        assert len(ArchitectureState) == 9

    def test_hyphenated_canonical_serialization(self) -> None:
        assert ArchitectureState.CTO_IMPLEMENTATION_REVIEWED.value == "CTO-IMPLEMENTATION-REVIEWED"
        assert ArchitectureState.CRO_VALIDATED.value == "CRO-VALIDATED"
        assert ArchitectureState.QUANT_VALIDATED.value == "QUANT-VALIDATED"

    def test_provenance_declared(self) -> None:
        assert ARCHITECTURE_STATE_SOURCE == "ARES-ARCHITECTURE-ANALYST-FRAMEWORK-001 §3"
        assert "ARES-ARCHITECTURE-ANALYST-FRAMEWORK-001 §3" in (ArchitectureState.__doc__ or "")


class TestAbsoluteSeparation:
    def test_distinct_types_no_inheritance(self) -> None:
        assert RosterState is not ArchitectureState
        assert not issubclass(RosterState, ArchitectureState)
        assert not issubclass(ArchitectureState, RosterState)

    def test_deprecated_homonym_is_not_the_same_member(self) -> None:
        assert RosterState.DEPRECATED is not ArchitectureState.DEPRECATED
        assert not isinstance(RosterState.DEPRECATED, ArchitectureState)
        assert not isinstance(ArchitectureState.DEPRECATED, RosterState)

    def test_no_cross_type_construction(self) -> None:
        # A value canonical in one vocabulary must not resolve in the other.
        with pytest.raises(ValueError):
            RosterState("CANDIDATE")
        with pytest.raises(ValueError):
            ArchitectureState("PLANNED")

    def test_no_crosswalk_exists_in_wu1(self) -> None:
        # The roster↔architecture mapping (and its NO MAPPING sentinel)
        # belongs to D2; WU-1 must not ship any mapping structure.
        source = inspect.getsource(lifecycle)
        for symbol in ("ROSTER_TO_ARCHITECTURE", "NO_MAPPING", "crosswalk_map"):
            assert symbol not in source


class TestWorkflowStatus31Excluded:
    def test_no_workflowstatus_type_anywhere_in_package(self) -> None:
        assert not hasattr(analysts_pkg, "WorkflowStatus")
        assert not hasattr(lifecycle, "WorkflowStatus")

    def test_no_31_only_tokens_as_values_or_names(self) -> None:
        enums = [
            obj
            for _, obj in vars(lifecycle).items()
            if inspect.isclass(obj) and issubclass(obj, RosterState.__bases__[1])
        ]
        assert enums, "expected at least the two D1 enums"
        for enum_cls in (RosterState, ArchitectureState):
            values = {m.value for m in enum_cls}
            names = set(enum_cls.__members__)
            for token in FORBIDDEN_31_ONLY_TOKENS:
                assert token not in values
                assert token not in names


class TestFailClosed:
    @pytest.mark.parametrize(
        "bad",
        ["", "tbd", "Planned", "NOT_A_STATE", "REQUESTED", "APPROVED "],
    )
    def test_unknown_roster_values_fail(self, bad: str) -> None:
        with pytest.raises(ValueError):
            RosterState(bad)

    @pytest.mark.parametrize(
        "bad",
        ["", "candidate", "CTO_IMPLEMENTATION_REVIEWED", "RESEARCHING", "PRODUCTION "],
    )
    def test_unknown_architecture_values_fail(self, bad: str) -> None:
        # NOTE: the underscore form of a hyphenated canonical value must fail.
        with pytest.raises(ValueError):
            ArchitectureState(bad)


class TestSerialization:
    def test_roster_round_trip_preserves_canonical_values(self) -> None:
        for member in RosterState:
            assert RosterState(member.value) is member
            assert json.loads(json.dumps(member.value)) == member.value

    def test_architecture_round_trip_preserves_canonical_values(self) -> None:
        for member in ArchitectureState:
            assert ArchitectureState(member.value) is member
            assert json.loads(json.dumps(member.value)) == member.value

    def test_no_silent_aliases(self) -> None:
        # @unique forbids duplicate values; also assert no alias names exist.
        assert len(RosterState.__members__) == len(list(RosterState)) == 15
        assert len(ArchitectureState.__members__) == len(list(ArchitectureState)) == 9
        assert len({m.value for m in RosterState}) == 15
        assert len({m.value for m in ArchitectureState}) == 9
