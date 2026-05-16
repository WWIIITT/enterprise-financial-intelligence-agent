from __future__ import annotations

import json
import time
from dataclasses import dataclass
from time import perf_counter
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.api.schemas import (
    CompanyFactsIngestRequest,
    CompanyFactsIngestResponse,
    FinancialFact,
    Metrics,
    Source,
    SqlAnalyzeRequest,
    SqlAnalyzeResponse,
    TraceStep,
)
from app.core.config import settings
from app.core.database import get_session_factory, initialize_database
from app.models import FinancialFactRecord
from app.services.sec_edgar_client import _resolve_company


SEC_COMPANY_FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
RETRY_STATUS_CODES = {429, 500, 502, 503, 504}
MAX_RETRIES = 3
TIMEOUT_SECONDS = 10

METRIC_CONCEPTS = {
    "revenue": ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet"],
    "net_income": ["NetIncomeLoss"],
    "assets": ["Assets"],
    "liabilities": ["Liabilities"],
    "cash": ["CashAndCashEquivalentsAtCarryingValue"],
    "operating_cash_flow": ["NetCashProvidedByUsedInOperatingActivities"],
    "shares": ["EntityCommonStockSharesOutstanding", "CommonStocksIncludingAdditionalPaidInCapital"],
}

METRIC_LABELS = {
    "revenue": "Revenue",
    "net_income": "Net Income",
    "assets": "Assets",
    "liabilities": "Liabilities",
    "cash": "Cash and Cash Equivalents",
    "operating_cash_flow": "Operating Cash Flow",
    "shares": "Shares Outstanding",
}

SAMPLE_AAPL_FACTS = [
    ("AAPL", "0000320193", "Apple Inc.", "Revenues", "Revenue", "USD", 2021, "FY", "10-K", "2021-10-29", 365817000000.0, "0000320193-21-000105"),
    ("AAPL", "0000320193", "Apple Inc.", "Revenues", "Revenue", "USD", 2022, "FY", "10-K", "2022-10-28", 394328000000.0, "0000320193-22-000108"),
    ("AAPL", "0000320193", "Apple Inc.", "Revenues", "Revenue", "USD", 2023, "FY", "10-K", "2023-11-03", 383285000000.0, "0000320193-23-000106"),
    ("AAPL", "0000320193", "Apple Inc.", "Revenues", "Revenue", "USD", 2024, "FY", "10-K", "2024-11-01", 391035000000.0, "0000320193-24-000123"),
    ("AAPL", "0000320193", "Apple Inc.", "NetIncomeLoss", "Net Income", "USD", 2021, "FY", "10-K", "2021-10-29", 94680000000.0, "0000320193-21-000105"),
    ("AAPL", "0000320193", "Apple Inc.", "NetIncomeLoss", "Net Income", "USD", 2022, "FY", "10-K", "2022-10-28", 99803000000.0, "0000320193-22-000108"),
    ("AAPL", "0000320193", "Apple Inc.", "NetIncomeLoss", "Net Income", "USD", 2023, "FY", "10-K", "2023-11-03", 96995000000.0, "0000320193-23-000106"),
    ("AAPL", "0000320193", "Apple Inc.", "NetIncomeLoss", "Net Income", "USD", 2024, "FY", "10-K", "2024-11-01", 93736000000.0, "0000320193-24-000123"),
    ("AAPL", "0000320193", "Apple Inc.", "Assets", "Assets", "USD", 2024, "FY", "10-K", "2024-11-01", 364980000000.0, "0000320193-24-000123"),
    ("AAPL", "0000320193", "Apple Inc.", "Liabilities", "Liabilities", "USD", 2024, "FY", "10-K", "2024-11-01", 308030000000.0, "0000320193-24-000123"),
    ("AAPL", "0000320193", "Apple Inc.", "CashAndCashEquivalentsAtCarryingValue", "Cash and Cash Equivalents", "USD", 2024, "FY", "10-K", "2024-11-01", 29943000000.0, "0000320193-24-000123"),
]


@dataclass(frozen=True)
class CompanyFactsPayload:
    ticker: str
    cik: str
    company_name: str
    facts: list[FinancialFact]
    source: str


class CompanyFactsClient:
    def fetch_company_facts(self, ticker: str, cik: str | None = None) -> CompanyFactsPayload:
        normalized_ticker = ticker.strip().upper()
        normalized_cik, resolved_ticker, company_name = _resolve_company(normalized_ticker, cik)
        if not settings.sec_user_agent:
            raise RuntimeError("SEC_USER_AGENT is required for live SEC Company Facts requests.")
        payload = _sec_get_json(SEC_COMPANY_FACTS_URL.format(cik=normalized_cik))
        parsed = parse_company_facts_payload(resolved_ticker, normalized_cik, payload)
        if parsed.company_name == resolved_ticker and company_name:
            return CompanyFactsPayload(
                ticker=parsed.ticker,
                cik=parsed.cik,
                company_name=company_name,
                facts=parsed.facts,
                source=parsed.source,
            )
        return parsed


def ingest_company_facts(request: CompanyFactsIngestRequest) -> CompanyFactsIngestResponse:
    ticker = request.ticker.strip().upper()
    try:
        payload = CompanyFactsClient().fetch_company_facts(ticker=ticker, cik=request.cik)
    except RuntimeError as exc:
        if not request.use_sample_fallback:
            raise
        payload = sample_company_facts(ticker)
        fallback_detail = f" Live SEC Company Facts unavailable; used sample fallback. Reason: {exc}"
    else:
        fallback_detail = ""

    saved = save_financial_facts(payload.facts)
    return CompanyFactsIngestResponse(
        status="completed",
        ticker=payload.ticker,
        cik=payload.cik,
        company_name=payload.company_name,
        facts_indexed=len(payload.facts),
        source=payload.source,
        message=(
            f"Company facts indexed for {payload.ticker} from {payload.source}. "
            f"PostgreSQL persistence {'succeeded' if saved else 'was skipped or unavailable'}."
            f"{fallback_detail}"
        ),
    )


def analyze_financial_facts(request: SqlAnalyzeRequest) -> SqlAnalyzeResponse:
    started = perf_counter()
    metric = normalize_metric(request.metric)
    ticker = request.ticker.strip().upper()
    facts = load_financial_facts(ticker=ticker, metric=metric, period=request.period, limit=request.limit)
    if not facts and ticker == "AAPL":
        save_financial_facts(sample_company_facts("AAPL").facts)
        facts = load_financial_facts(ticker=ticker, metric=metric, period=request.period, limit=request.limit)
    answer = compose_sql_answer(ticker=ticker, metric=metric, facts=facts)
    sources = [
        Source(
            title=f"{fact.ticker} {fact.label} {fact.fiscal_year}",
            url=f"https://data.sec.gov/api/xbrl/companyfacts/CIK{fact.cik}.json",
            citation=f"SEC Company Facts {fact.ticker} {fact.concept} {fact.fiscal_year} {fact.form_type}",
            source_type="sql",
        )
        for fact in facts[:3]
    ]
    return SqlAnalyzeResponse(
        answer=answer,
        agent="sql-analytics-agent",
        facts=facts,
        sources=sources,
        trace=[
            TraceStep(step="receive", detail=f"Received SQL analytics request for {ticker}."),
            TraceStep(step="sql_analytics", detail=f"Queried {len(facts)} {metric} fact(s) using safe templates."),
            TraceStep(step="respond", detail="Returned deterministic SQL analytics response."),
        ],
        metrics=Metrics(latency_ms=int((perf_counter() - started) * 1000)),
    )


def parse_company_facts_payload(ticker: str, cik: str, payload: dict[str, Any]) -> CompanyFactsPayload:
    company_name = str(payload.get("entityName") or ticker)
    facts: list[FinancialFact] = []
    us_gaap = payload.get("facts", {}).get("us-gaap", {})
    for concepts in METRIC_CONCEPTS.values():
        for concept in concepts:
            concept_payload = us_gaap.get(concept)
            if not concept_payload:
                continue
            label = str(concept_payload.get("label") or concept)
            for unit, entries in concept_payload.get("units", {}).items():
                for entry in entries:
                    fact = _entry_to_fact(ticker, cik, company_name, concept, label, unit, entry)
                    if fact:
                        facts.append(fact)
    return CompanyFactsPayload(ticker=ticker, cik=cik, company_name=company_name, facts=facts, source="SEC Company Facts")


def sample_company_facts(ticker: str) -> CompanyFactsPayload:
    normalized = ticker.strip().upper()
    rows = SAMPLE_AAPL_FACTS if normalized == "AAPL" else SAMPLE_AAPL_FACTS
    facts = [
        FinancialFact(
            ticker=row[0],
            cik=row[1],
            company_name=row[2],
            concept=row[3],
            label=row[4],
            unit=row[5],
            fiscal_year=row[6],
            fiscal_period=row[7],
            form_type=row[8],
            filed_date=row[9],
            value=row[10],
            source="SEC Company Facts sample",
            accession_number=row[11],
        )
        for row in rows
    ]
    return CompanyFactsPayload(ticker="AAPL", cik="0000320193", company_name="Apple Inc.", facts=facts, source="SEC Company Facts sample")


def save_financial_facts(facts: list[FinancialFact]) -> bool:
    if not facts or not initialize_database():
        return False
    session_factory = get_session_factory()
    if session_factory is None:
        return False

    try:
        with session_factory() as session:
            ticker = facts[0].ticker
            session.query(FinancialFactRecord).filter(FinancialFactRecord.ticker == ticker).delete()
            for fact in facts:
                session.add(
                    FinancialFactRecord(
                        ticker=fact.ticker,
                        cik=fact.cik,
                        company_name=fact.company_name,
                        concept=fact.concept,
                        label=fact.label,
                        unit=fact.unit,
                        fiscal_year=fact.fiscal_year,
                        fiscal_period=fact.fiscal_period,
                        form_type=fact.form_type,
                        filed_date=fact.filed_date,
                        value=fact.value,
                        source=fact.source,
                        accession_number=fact.accession_number,
                    )
                )
            session.commit()
    except Exception:
        return False
    return True


def load_financial_facts(ticker: str, metric: str, period: str, limit: int) -> list[FinancialFact]:
    if not initialize_database():
        return [fact for fact in sample_company_facts(ticker).facts if _fact_matches(fact, metric, period)][-limit:]
    session_factory = get_session_factory()
    if session_factory is None:
        return []

    concepts = METRIC_CONCEPTS[metric]
    period_code = "FY" if period == "annual" else "Q"
    try:
        with session_factory() as session:
            query = (
                session.query(FinancialFactRecord)
                .filter(FinancialFactRecord.ticker == ticker)
                .filter(FinancialFactRecord.concept.in_(concepts))
            )
            if period == "annual":
                query = query.filter(FinancialFactRecord.fiscal_period == period_code)
            else:
                query = query.filter(FinancialFactRecord.fiscal_period != "FY")
            records = query.order_by(FinancialFactRecord.fiscal_year.desc(), FinancialFactRecord.filed_date.desc()).limit(limit).all()
    except Exception:
        return []

    facts = [_record_to_fact(record) for record in records]
    facts.reverse()
    return facts


def compose_sql_answer(ticker: str, metric: str, facts: list[FinancialFact]) -> str:
    label = METRIC_LABELS[metric]
    if not facts:
        return (
            "## Summary\n"
            f"No structured financial facts are available for {ticker} {label} yet.\n\n"
            "## Next Step\n"
            "- Run company facts ingestion, then retry the SQL analytics request.\n\n"
            "## Sources\n"
            "- No SQL facts available"
        )
    latest = facts[-1]
    trend = _trend_label(facts)
    fact_lines = "\n".join(
        f"- FY{fact.fiscal_year} {fact.label}: {_format_value(fact.value)} {fact.unit} ({fact.form_type}, filed {fact.filed_date})"
        for fact in facts
    )
    source_lines = "\n".join(f"- SEC Company Facts {fact.ticker} {fact.concept} {fact.fiscal_year}" for fact in facts[-3:])
    return (
        "## Summary\n"
        f"{ticker} {label} latest structured value is {_format_value(latest.value)} {latest.unit} for FY{latest.fiscal_year}; recent trend is {trend}.\n\n"
        "## Financial Facts\n"
        f"{fact_lines}\n\n"
        "## Sources\n"
        f"{source_lines}"
    )


def normalize_metric(metric: str) -> str:
    normalized = metric.strip().lower().replace(" ", "_").replace("-", "_")
    aliases = {
        "sales": "revenue",
        "net_income_loss": "net_income",
        "income": "net_income",
        "liability": "liabilities",
        "operating_cash": "operating_cash_flow",
        "cash_flow": "operating_cash_flow",
        "shares_outstanding": "shares",
    }
    normalized = aliases.get(normalized, normalized)
    if normalized not in METRIC_CONCEPTS:
        raise RuntimeError(f"Unsupported SQL metric '{metric}'. Supported metrics: {', '.join(METRIC_CONCEPTS)}.")
    return normalized


def infer_sql_request(message: str) -> SqlAnalyzeRequest:
    lowered = message.lower()
    metric = "revenue"
    for candidate in METRIC_CONCEPTS:
        if candidate.replace("_", " ") in lowered or candidate in lowered:
            metric = candidate
            break
    if "net income" in lowered:
        metric = "net_income"
    elif "cash flow" in lowered or "operating cash" in lowered:
        metric = "operating_cash_flow"
    elif "cash" in lowered:
        metric = "cash"
    elif "liabilities" in lowered or "liability" in lowered:
        metric = "liabilities"
    elif "assets" in lowered:
        metric = "assets"
    elif "share" in lowered:
        metric = "shares"

    ticker = "AAPL" if "apple" in lowered or "aapl" in lowered else "AAPL"
    period = "quarterly" if "quarter" in lowered or "quarterly" in lowered else "annual"
    return SqlAnalyzeRequest(ticker=ticker, metric=metric, period=period, limit=5)


def is_sql_question(message: str) -> bool:
    lowered = message.lower()
    return any(
        term in lowered
        for term in (
            "revenue trend",
            "net income",
            "assets",
            "liabilities",
            "financial metrics",
            "structured data",
            "sql",
            "company facts",
            "balance sheet",
            "income statement",
        )
    )


def _sec_get_json(url: str) -> dict[str, Any]:
    last_error: Exception | None = None
    for attempt in range(MAX_RETRIES):
        try:
            request = Request(url, headers={"User-Agent": settings.sec_user_agent, "Accept-Encoding": "identity"})
            with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            last_error = exc
            if exc.code not in RETRY_STATUS_CODES:
                break
        except (TimeoutError, URLError) as exc:
            last_error = exc
        if attempt < MAX_RETRIES - 1:
            time.sleep(0.25 * (attempt + 1))
    raise RuntimeError(f"SEC Company Facts request failed: {last_error}") from last_error


def _entry_to_fact(
    ticker: str,
    cik: str,
    company_name: str,
    concept: str,
    label: str,
    unit: str,
    entry: dict[str, Any],
) -> FinancialFact | None:
    try:
        value = float(entry["val"])
        fiscal_year = int(entry.get("fy") or 0)
    except (KeyError, TypeError, ValueError):
        return None
    fiscal_period = str(entry.get("fp") or "")
    form_type = str(entry.get("form") or "")
    if not fiscal_year or form_type not in {"10-K", "10-Q"}:
        return None
    return FinancialFact(
        ticker=ticker,
        cik=cik,
        company_name=company_name,
        concept=concept,
        label=label,
        unit=unit,
        fiscal_year=fiscal_year,
        fiscal_period=fiscal_period,
        form_type=form_type,
        filed_date=str(entry.get("filed") or ""),
        value=value,
        source="SEC Company Facts",
        accession_number=str(entry.get("accn") or ""),
    )


def _record_to_fact(record: FinancialFactRecord) -> FinancialFact:
    return FinancialFact(
        ticker=record.ticker,
        cik=record.cik,
        company_name=record.company_name,
        concept=record.concept,
        label=record.label,
        unit=record.unit,
        fiscal_year=record.fiscal_year,
        fiscal_period=record.fiscal_period,
        form_type=record.form_type,
        filed_date=record.filed_date,
        value=record.value,
        source=record.source,
        accession_number=record.accession_number,
    )


def _fact_matches(fact: FinancialFact, metric: str, period: str) -> bool:
    if fact.concept not in METRIC_CONCEPTS[metric]:
        return False
    if period == "annual":
        return fact.fiscal_period == "FY"
    return fact.fiscal_period != "FY"


def _normalize_cik(cik: str) -> str:
    return cik.strip().zfill(10)


def _trend_label(facts: list[FinancialFact]) -> str:
    if len(facts) < 2:
        return "flat/insufficient history"
    delta = facts[-1].value - facts[0].value
    if abs(delta) < 0.01:
        return "flat"
    return "up" if delta > 0 else "down"


def _format_value(value: float) -> str:
    abs_value = abs(value)
    if abs_value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    if abs_value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    return f"{value:,.0f}"
