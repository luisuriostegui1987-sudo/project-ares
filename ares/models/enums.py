"""Canonical enumerations for Project ARES.

Every value here is authoritative per ARES-015 (Canonical Glossary & Data
Dictionary). Do not redefine these elsewhere; import from this module.
"""
from __future__ import annotations

from enum import Enum


class KnowledgeClass(str, Enum):
    """RULE 17 epistemic classes — how sure we are a claim is TRUE.

    Distinct from :class:`ProcessState`, which describes the state of work.
    """

    VERIFIED_FACT = "Verified Fact"
    HIGH_CONFIDENCE = "High Confidence"
    REASONABLE_INFERENCE = "Reasonable Inference"
    SPECULATION = "Speculation"
    OPINION = "Opinion"
    UNKNOWN = "Unknown"

    @property
    def usable_for_calculation(self) -> bool:
        """Only Verified Fact / High Confidence may feed deterministic calcs.

        Enforces Constitution Sec 5 (anti-hallucination) and ARES-003 Sec 5.3.
        """
        return self in (KnowledgeClass.VERIFIED_FACT, KnowledgeClass.HIGH_CONFIDENCE)


class ProcessState(str, Enum):
    """Operational states — the state of work, NOT a truth class."""

    CONFLICTED = "CONFLICTED"
    MISSING = "MISSING"


class Direction(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"
    NEUTRAL = "NEUTRAL"


class TimeHorizon(str, Enum):
    """Primary v1 horizons (Constitution Sec 7 / ARES-002)."""

    TWO_WEEKS = "2W"
    ONE_MONTH = "1M"
    THREE_MONTHS = "3M"
    SIX_MONTHS = "6M"


class EventType(str, Enum):
    EARNINGS = "EARNINGS"
    GUIDANCE = "GUIDANCE"
    PRODUCT_LAUNCH = "PRODUCT_LAUNCH"
    REGULATORY = "REGULATORY"
    CONTRACT = "CONTRACT"
    MACRO = "MACRO"
    INDEX_CHANGE = "INDEX_CHANGE"
    LOCKUP_EXPIRY = "LOCKUP_EXPIRY"
    OTHER = "OTHER"


class RiskVerdict(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    NEEDS_REVIEW = "NEEDS_REVIEW"


class InvestmentDecisionType(str, Enum):
    """Human actions recorded in the Paper Decision Ledger (ARES-015)."""

    APPROVE = "APPROVE"
    REJECT = "REJECT"
    MORE_RESEARCH = "MORE_RESEARCH"
    WATCHLIST = "WATCHLIST"


class ThesisStatus(str, Enum):
    DRAFT = "Draft"
    CHALLENGED = "Challenged"
    SCORED = "Scored"
    PRESENTED = "Presented"
    CLOSED = "Closed"


class ClaimType(str, Enum):
    """Coarse view of KnowledgeClass (ARES-015 reconciliation note)."""

    FACTUAL = "factual"
    INFERENTIAL = "inferential"
    SPECULATIVE = "speculative"
    OPINION = "opinion"
