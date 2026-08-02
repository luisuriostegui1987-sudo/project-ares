"""SEC EDGAR live provider (Sprint 2).

Official structured endpoints only (no HTML scraping):
- ticker -> CIK:   https://www.sec.gov/files/company_tickers.json
- company facts:   https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json

SEC fair-access compliance: declarative User-Agent with contact, request rate
limiting, timeouts and bounded retries.

Every extracted datum becomes an InstitutionalFact (ARES-FACT-001) preserving
accession number, form, filing date, fiscal period, XBRL concept and unit in
source_locator. A value is Verified Fact ONLY when the full provenance and
extraction requirements pass; otherwise it is downgraded.

Live mode NEVER falls back to mock data: any failure raises EdgarError.
"""

from __future__ import annotations

import json
import logging
import os
import time
import urllib.error
import urllib.request
from datetime import UTC, date, datetime, timedelta
from typing import Any

from ares.facts import InMemoryFactStore
from ares.models import Entity, Event, Fact, KnowledgeClass
from ares.models.base import utcnow
from ares.models.ifact import (
    FactValidationEvent,
    InstitutionalFact,
    are_comparable,
    canonical_value,
)
from ares.models.vocab import (
    METRIC_REGISTRY,
    AssertionType,
    Basis,
    PeriodType,
    ProvenanceType,
    RetrievalMethod,
    ValidationStatus,
)
from ares.pipeline.context import EntityContext
from ares.pipeline.facts import METRIC_REVENUE_FY_CURRENT, METRIC_REVENUE_FY_PRIOR

logger = logging.getLogger(__name__)

EXTRACTOR_VERSION = "EDGAR-1.0"
SOURCE_ID = "sec.edgar"
TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
COMPANY_FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"

# Approved XBRL concept mapping (Sprint 2). Order matters: first present wins.
# Deliberately tiny — mapping the whole taxonomy is out of scope.
CONCEPT_MAP: dict[str, tuple[tuple[str, str], ...]] = {
    "financial.revenue": (
        ("us-gaap", "RevenueFromContractWithCustomerExcludingAssessedTax"),
        ("us-gaap", "Revenues"),
        ("us-gaap", "SalesRevenueNet"),
    ),
    "financial.net_income": (("us-gaap", "NetIncomeLoss"),),
    "financial.diluted_eps": (("us-gaap", "EarningsPerShareDiluted"),),
    "financial.gross_profit": (("us-gaap", "GrossProfit"),),
    "financial.operating_income": (("us-gaap", "OperatingIncomeLoss"),),
    "financial.cash_and_equivalents": (("us-gaap", "CashAndCashEquivalentsAtCarryingValue"),),
    "financial.total_assets": (("us-gaap", "Assets"),),
    "financial.total_liabilities": (("us-gaap", "Liabilities"),),
    "financial.shares_outstanding": (
        ("dei", "EntityCommonStockSharesOutstanding"),
        ("us-gaap", "CommonStockSharesOutstanding"),
    ),
}

_UNIT_CURRENCY = {"USD": "USD", "USD/shares": "USD", "shares": None}

# (taxonomy, xbrl tag, unit, raw companyfacts item)
TaggedItem = tuple[str, str, str, dict[str, Any]]


class EdgarError(RuntimeError):
    """Live EDGAR retrieval failed. Never silently replaced by mock data."""


def default_user_agent() -> str:
    return os.environ.get(
        "ARES_SEC_USER_AGENT",
        "Project ARES research client (contact: luisuriostegui1987@gmail.com)",
    )


class EdgarClient:
    """Minimal SEC client: official endpoints, UA, rate limit, timeout, retry."""

    def __init__(
        self,
        user_agent: str | None = None,
        timeout: float = 10.0,
        max_retries: int = 3,
        min_interval: float = 0.25,
    ) -> None:
        self.user_agent = user_agent or default_user_agent()
        self.timeout = timeout
        self.max_retries = max_retries
        self.min_interval = min_interval
        self._last_request = 0.0
        self._cache: dict[str, Any] = {}

    def _get_json(self, url: str) -> Any:
        if url in self._cache:
            return self._cache[url]
        last_error: Exception | None = None
        for attempt in range(1, self.max_retries + 1):
            wait = self.min_interval - (time.monotonic() - self._last_request)
            if wait > 0:
                time.sleep(wait)
            self._last_request = time.monotonic()
            request = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    payload = json.loads(response.read().decode("utf-8"))
                self._cache[url] = payload
                return payload
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
                last_error = exc
                logger.warning(
                    "edgar: attempt %d/%d failed for %s: %s", attempt, self.max_retries, url, exc
                )
                time.sleep(min(2.0 * attempt, 5.0))
        raise EdgarError(f"SEC request failed after {self.max_retries} attempts: {url}") from (
            last_error
        )

    def cik_for_ticker(self, ticker: str) -> int:
        data = self._get_json(TICKERS_URL)
        for row in data.values():
            if str(row.get("ticker", "")).upper() == ticker.upper():
                return int(row["cik_str"])
        raise EdgarError(f"Ticker {ticker!r} not found in SEC company_tickers.json.")

    def company_name_for_ticker(self, ticker: str) -> str:
        data = self._get_json(TICKERS_URL)
        for row in data.values():
            if str(row.get("ticker", "")).upper() == ticker.upper():
                return str(row.get("title", ticker)).strip()
        raise EdgarError(f"Ticker {ticker!r} not found in SEC company_tickers.json.")

    def company_facts(self, cik: int) -> dict[str, Any]:
        payload = self._get_json(COMPANY_FACTS_URL.format(cik=cik))
        if not isinstance(payload, dict) or "facts" not in payload:
            raise EdgarError(f"Malformed companyfacts payload for CIK {cik}.")
        return payload


# ---- extraction: companyfacts JSON -> InstitutionalFacts ---------------------


def _parse_date(raw: str | None) -> datetime | None:
    if not raw:
        return None
    return datetime.combine(date.fromisoformat(raw), datetime.min.time(), tzinfo=UTC)


def _source_locator(cik: int, item: dict[str, Any], taxonomy: str, tag: str, unit: str) -> str:
    """Exact provenance: accession, form, filing date, fiscal period, concept, unit."""
    return (
        f"edgar:cik={cik};accn={item.get('accn', '')};form={item.get('form', '')};"
        f"filed={item.get('filed', '')};fy={item.get('fy', '')};fp={item.get('fp', '')};"
        f"concept={taxonomy}:{tag};unit={unit}"
    )


def _provenance_complete(item: dict[str, Any]) -> bool:
    """Verified Fact requires full provenance + extraction requirements."""
    return bool(
        item.get("accn")
        and item.get("form")
        and item.get("filed")
        and item.get("end")
        and isinstance(item.get("val"), (int, float))
    )


def extract_institutional_facts(
    ticker: str,
    cik: int,
    payload: dict[str, Any],
    retrieved_at: datetime | None = None,
    annual_years: int = 2,
) -> list[InstitutionalFact]:
    """Deterministically map the approved XBRL subset to InstitutionalFacts."""
    retrieved = retrieved_at or utcnow()
    facts: list[InstitutionalFact] = []
    taxonomies: dict[str, Any] = payload.get("facts", {})

    for metric_ref, concepts in CONCEPT_MAP.items():
        spec = METRIC_REGISTRY[metric_ref]
        # Merge candidates across ALL mapped concepts: issuers switch XBRL tags
        # between years, so picking the first tag with data can strand a metric
        # on stale fiscal years.
        tagged: list[TaggedItem] = []
        for taxonomy, tag in concepts:
            concept_data = taxonomies.get(taxonomy, {}).get(tag)
            if not concept_data:
                continue
            for unit_name, items in concept_data.get("units", {}).items():
                if unit_name not in _UNIT_CURRENCY:
                    continue
                tagged.extend((taxonomy, tag, unit_name, item) for item in items)
                break  # one unit per concept
        if not tagged:
            logger.info("edgar: %s has no data for %s (MISSING)", ticker, metric_ref)
            continue

        if spec.period_type is PeriodType.DURATION:
            selected = _latest_annual(tagged, annual_years)
        else:
            selected = _latest_instants(tagged, 1)
        for taxonomy, tag, unit_name, item in selected:
            fact = _to_institutional_fact(
                ticker,
                cik,
                metric_ref,
                spec.value_type,
                spec.period_type,
                taxonomy,
                tag,
                unit_name,
                item,
                retrieved,
            )
            if fact is not None:
                facts.append(fact)
    return facts


def _latest_annual(tagged: list[TaggedItem], count: int) -> list[TaggedItem]:
    """Latest N distinct fiscal-year 10-K duration entries (~annual periods)."""
    annual: dict[str, TaggedItem] = {}
    for taxonomy, tag, unit, item in tagged:
        if item.get("form") != "10-K" or item.get("fp") != "FY":
            continue
        # NOTE: entries carrying a "frame" annotation are still real filed data
        # (accession/form/filed preserved); they dedupe by period below.
        start, end = item.get("start"), item.get("end")
        if not start or not end:
            continue
        try:
            span = (date.fromisoformat(end) - date.fromisoformat(start)).days
        except ValueError:
            continue
        if not 300 <= span <= 400:  # a fiscal year, not a quarter
            continue
        prev = annual.get(end)
        if prev is None or str(item.get("filed", "")) > str(prev[3].get("filed", "")):
            annual[end] = (taxonomy, tag, unit, item)
    ordered = sorted(annual.values(), key=lambda t: str(t[3]["end"]), reverse=True)
    return ordered[:count]


def _latest_instants(tagged: list[TaggedItem], count: int) -> list[TaggedItem]:
    """Latest N instant entries from real filings."""
    by_end: dict[str, TaggedItem] = {}
    for taxonomy, tag, unit, item in tagged:
        end = item.get("end")
        if not end:
            continue
        prev = by_end.get(end)
        if prev is None or str(item.get("filed", "")) > str(prev[3].get("filed", "")):
            by_end[end] = (taxonomy, tag, unit, item)
    ordered = sorted(by_end.values(), key=lambda t: str(t[3]["end"]), reverse=True)
    return ordered[:count]


def _to_institutional_fact(
    ticker: str,
    cik: int,
    metric_ref: str,
    value_type: Any,
    period_type: PeriodType,
    taxonomy: str,
    tag: str,
    unit_name: str,
    item: dict[str, Any],
    retrieved: datetime,
) -> InstitutionalFact | None:
    value = item.get("val")
    if not isinstance(value, (int, float)):
        return None
    published = _parse_date(item.get("filed"))
    end = _parse_date(item.get("end"))
    if published is None or end is None:
        return None
    knowledge = (
        KnowledgeClass.VERIFIED_FACT
        if _provenance_complete(item)
        else KnowledgeClass.HIGH_CONFIDENCE
    )
    common: dict[str, Any] = {
        "subject_entity_id": ticker,
        "subject_scope_type": "COMPANY",
        "subject_scope_id": f"CIK{cik:010d}",
        "metric_ref": metric_ref,
        "basis": Basis.AS_REPORTED,
        "assertion_type": AssertionType.REPORTED,
        "value": value,
        "value_type": value_type,
        "unit": unit_name,
        "currency": _UNIT_CURRENCY.get(unit_name),
        "period_type": period_type,
        "published_at": published,
        "retrieved_at": retrieved,
        "source_id": SOURCE_ID,
        "source_locator": _source_locator(cik, item, taxonomy, tag, unit_name),
        "provenance_type": ProvenanceType.PRIMARY,
        "retrieval_method": RetrievalMethod.API,
        "knowledge_class": knowledge,
        "ingested_by": "ares.providers.edgar",
        "extractor_version": EXTRACTOR_VERSION,
    }
    if period_type is PeriodType.INSTANT:
        common["effective_instant"] = end
    else:
        start = _parse_date(item.get("start"))
        if start is None:
            return None
        common["effective_start"] = start
        common["effective_end"] = end
    return InstitutionalFact(**common)


# ---- live pipeline providers -------------------------------------------------


class EdgarEntityProvider:
    """Resolves a ticker through the official SEC ticker file."""

    def __init__(self, client: EdgarClient) -> None:
        self.client = client

    def resolve(self, ticker: str) -> Entity:
        name = self.client.company_name_for_ticker(ticker)
        return Entity(entity_id=ticker, ticker=ticker, name=name)


class LiveContextProvider:
    """Minimal live context. No mock narrative is ever used in LIVE mode."""

    def __init__(self, client: EdgarClient) -> None:
        self.client = client

    def context_for(self, entity: Entity) -> EntityContext:
        cik = self.client.cik_for_ticker(entity.ticker)
        entity_name = self.client.company_facts(cik).get("entityName", entity.name)
        return EntityContext(
            entity_id=entity.entity_id,
            business_summary=(
                f"{entity_name} (SEC CIK {cik:010d}). LIVE EDGAR mode: qualitative "
                "business context is not ingested in Sprint 2."
            ),
        )


class NoEventsProvider:
    """LIVE mode ships no event calendar in Sprint 2; empty is a valid outcome."""

    def events_for(self, entity: Entity) -> list[Event]:
        return []


class EdgarFactsProvider:
    """Live FactsProvider: EDGAR -> InstitutionalFacts (stored) -> pipeline Facts."""

    def __init__(self, client: EdgarClient, store: InMemoryFactStore | None = None) -> None:
        self.client = client
        self.store = store or InMemoryFactStore()

    def facts_for(self, entity: Entity) -> list[Fact]:
        cik = self.client.cik_for_ticker(entity.ticker)
        payload = self.client.company_facts(cik)
        ifacts = extract_institutional_facts(entity.ticker, cik, payload)
        if not ifacts:
            raise EdgarError(f"EDGAR returned no mappable facts for {entity.ticker}.")
        stored: list[InstitutionalFact] = []
        for ifact in ifacts:
            kept = self.store.append(ifact)
            self.store.add_validation_event(
                FactValidationEvent(
                    fact_id=kept.fact_id,
                    status=ValidationStatus.VALID,
                    reason="Deterministic EDGAR extraction with complete provenance.",
                    recorded_by="ares.providers.edgar",
                )
            )
            stored.append(kept)
        return _to_pipeline_facts(entity, stored)


def _to_pipeline_facts(entity: Entity, ifacts: list[InstitutionalFact]) -> list[Fact]:
    """Adapt InstitutionalFacts to the Sprint-1 report contract, keeping ids."""
    out: list[Fact] = []
    revenue = sorted(
        (f for f in ifacts if f.metric_ref == "financial.revenue"),
        key=lambda f: f.effective_end or f.retrieved_at,
        reverse=True,
    )
    named: list[tuple[str, InstitutionalFact, float | int | str]] = []
    if revenue:
        current = revenue[0]
        current_value: float | int | str = current.value
        # Fail closed (CRO): the YoY pair is only formed when the canonical
        # comparability predicate passes — otherwise the prior name is never
        # emitted and no growth signal can exist downstream.
        if len(revenue) >= 2:
            prior = revenue[1]
            if are_comparable(current, prior):
                # Equal scales: raw values already share the canonical scale.
                named.append((METRIC_REVENUE_FY_PRIOR, prior, prior.value))
            elif are_comparable(current, prior, canonical_scale=0):
                # Explicit normalization to canonical scale 0: BOTH values go
                # through canonical_value(); growth math downstream never
                # mixes unnormalized raw values.
                current_canonical = canonical_value(current)
                prior_canonical = canonical_value(prior)
                if current_canonical is not None and prior_canonical is not None:
                    current_value = current_canonical
                    named.append((METRIC_REVENUE_FY_PRIOR, prior, prior_canonical))
            else:
                logger.warning(
                    "edgar: revenue pair for %s failed the comparability predicate; "
                    "no YoY pair emitted",
                    entity.entity_id,
                )
        named.insert(0, (METRIC_REVENUE_FY_CURRENT, current, current_value))
    seen_metrics: set[str] = set()
    for f in ifacts:
        if f.metric_ref == "financial.revenue" or f.metric_ref in seen_metrics:
            continue
        seen_metrics.add(f.metric_ref)
        named.append((f.metric_ref, f, f.value))
    for metric_name, ifact, value in named:
        out.append(
            Fact(
                fact_id=ifact.fact_id,  # same record id: report cites the store
                entity_id=entity.entity_id,
                metric_name=metric_name,
                value=value,
                unit=ifact.currency or ifact.unit,
                source_name="SEC EDGAR",
                source_id_or_url=ifact.source_locator,
                as_of_timestamp=ifact.effective_instant or ifact.effective_end or utcnow(),
                knowledge_class=ifact.knowledge_class,
                retrieved_at=ifact.retrieved_at,
            )
        )
    return out


def freshness_horizon(published_at: datetime, days: int = 400) -> datetime:
    """Simple deterministic freshness horizon for annual filings."""
    return published_at + timedelta(days=days)
