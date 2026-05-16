from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import datetime, timezone
from time import perf_counter
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from app.api.schemas import MacroAnalyzeRequest, MacroAnalyzeResponse, MacroSeriesResponse, Metrics, Source, TraceStep
from app.core.config import settings
from app.core.database import get_session_factory, initialize_database
from app.models import MacroObservationRecord


FRED_OBSERVATIONS_URL = "https://api.stlouisfed.org/fred/series/observations"
FRED_SERIES_URL = "https://api.stlouisfed.org/fred/series"
FRED_RETRY_STATUS_CODES = {429, 500, 502, 503, 504}
FRED_MAX_RETRIES = 3
FRED_TIMEOUT_SECONDS = 8

MACRO_SERIES = {
    "FEDFUNDS": {"title": "Federal Funds Effective Rate", "units": "Percent"},
    "CPIAUCSL": {"title": "Consumer Price Index for All Urban Consumers", "units": "Index 1982-1984=100"},
    "UNRATE": {"title": "Unemployment Rate", "units": "Percent"},
    "GDP": {"title": "Gross Domestic Product", "units": "Billions of dollars"},
    "DGS10": {"title": "10-Year Treasury Constant Maturity Rate", "units": "Percent"},
}

SAMPLE_OBSERVATIONS = {
    "FEDFUNDS": [
        {"date": "2025-08-01", "value": 4.33},
        {"date": "2025-09-01", "value": 4.22},
        {"date": "2025-10-01", "value": 4.09},
    ],
    "CPIAUCSL": [
        {"date": "2025-08-01", "value": 322.13},
        {"date": "2025-09-01", "value": 323.01},
        {"date": "2025-10-01", "value": 323.85},
    ],
    "UNRATE": [
        {"date": "2025-08-01", "value": 4.2},
        {"date": "2025-09-01", "value": 4.1},
        {"date": "2025-10-01", "value": 4.2},
    ],
    "GDP": [
        {"date": "2025-01-01", "value": 29349.92},
        {"date": "2025-04-01", "value": 29518.44},
        {"date": "2025-07-01", "value": 29702.31},
    ],
    "DGS10": [
        {"date": "2025-10-27", "value": 4.00},
        {"date": "2025-10-28", "value": 3.98},
        {"date": "2025-10-29", "value": 4.07},
    ],
}


@dataclass(frozen=True)
class MacroSeriesData:
    series_id: str
    title: str
    units: str
    observations: list[dict[str, str | float]]
    source: str
    cache_status: str


class FredClient:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key if api_key is not None else settings.fred_api_key

    def fetch_series(self, series_id: str, limit: int = 12) -> MacroSeriesData:
        normalized = _normalize_series_id(series_id)
        if not self.api_key:
            return _sample_series(normalized, limit, cache_status="sample-fallback")

        metadata = self._fetch_metadata(normalized)
        observations = self._fetch_observations(normalized, limit)
        return MacroSeriesData(
            series_id=normalized,
            title=str(metadata.get("title") or MACRO_SERIES.get(normalized, {}).get("title", normalized)),
            units=str(metadata.get("units") or MACRO_SERIES.get(normalized, {}).get("units", "")),
            observations=observations,
            source="FRED",
            cache_status="live",
        )

    def _fetch_metadata(self, series_id: str) -> dict[str, Any]:
        payload = _fred_get_json(
            FRED_SERIES_URL,
            {
                "series_id": series_id,
                "api_key": self.api_key,
                "file_type": "json",
            },
        )
        series = payload.get("seriess") or []
        return series[0] if series else {}

    def _fetch_observations(self, series_id: str, limit: int) -> list[dict[str, str | float]]:
        payload = _fred_get_json(
            FRED_OBSERVATIONS_URL,
            {
                "series_id": series_id,
                "api_key": self.api_key,
                "file_type": "json",
                "sort_order": "desc",
                "limit": str(limit),
            },
        )
        observations: list[dict[str, str | float]] = []
        for item in payload.get("observations", []):
            value = _parse_float(item.get("value"))
            if value is None:
                continue
            observations.append({"date": str(item.get("date", "")), "value": value})
        observations.reverse()
        return observations


def get_macro_series(series_id: str, limit: int = 12, refresh: bool = False, client: FredClient | None = None) -> MacroSeriesResponse:
    normalized = _normalize_series_id(series_id)
    if not refresh:
        cached = _load_cached_series(normalized, limit)
        if cached:
            return _series_response(cached)

    fred_client = client or FredClient()
    try:
        data = fred_client.fetch_series(normalized, limit)
    except RuntimeError:
        data = _sample_series(normalized, limit, cache_status="sample-fallback-after-error")

    _save_macro_observations(data)
    return _series_response(data)


def analyze_macro_context(request: MacroAnalyzeRequest) -> MacroAnalyzeResponse:
    start = perf_counter()
    unique_series = _dedupe_series(request.series_ids)
    series = [get_macro_series(series_id, limit=request.limit) for series_id in unique_series]
    answer = compose_macro_answer(request.question, series)
    latency_ms = int((perf_counter() - start) * 1000)
    return MacroAnalyzeResponse(
        answer=answer,
        agent="macro-analysis-agent",
        series=series,
        sources=[
            Source(
                title=item.title or item.series_id,
                url=f"https://fred.stlouisfed.org/series/{item.series_id}",
                citation=f"FRED {item.series_id}",
                source_type="macro",
            )
            for item in series
        ],
        trace=[
            TraceStep(step="receive", detail=f"Received macro question with {len(request.series_ids)} requested series."),
            TraceStep(step="macro", detail=f"Loaded {len(series)} macro series from FRED/cache/sample data."),
            TraceStep(step="respond", detail="Returned deterministic macro summary with citations."),
        ],
        metrics=Metrics(latency_ms=latency_ms),
    )


def compose_macro_answer(question: str, series: list[MacroSeriesResponse], sec_citations: list[str] | None = None) -> str:
    macro_lines = [_series_summary_line(item) for item in series if item.observations]
    source_lines = [f"- FRED {item.series_id}" for item in series]
    if sec_citations:
        source_lines.extend(f"- {citation}" for citation in sec_citations[:3])

    linkage = _macro_linkage_text(question)
    return (
        "## Summary\n"
        "Macro context is based on indexed FRED series and deterministic trend checks.\n\n"
        "## Macro Context\n"
        f"{chr(10).join(f'- {line}' for line in macro_lines) if macro_lines else '- No macro observations available.'}\n\n"
        "## Company Risk Linkage\n"
        f"- {linkage}\n\n"
        "## Sources\n"
        f"{chr(10).join(source_lines)}"
    )


def is_macro_question(question: str) -> bool:
    lowered = question.lower()
    return any(
        term in lowered
        for term in (
            "macro",
            "interest rate",
            "interest rates",
            "inflation",
            "cpi",
            "unemployment",
            "gdp",
            "fed funds",
            "treasury",
            "yield",
            "rates",
        )
    )


def infer_macro_series(question: str) -> list[str]:
    lowered = question.lower()
    selected: list[str] = []
    if any(term in lowered for term in ("interest", "rate", "rates", "fed funds")):
        selected.append("FEDFUNDS")
    if any(term in lowered for term in ("inflation", "cpi", "price")):
        selected.append("CPIAUCSL")
    if "unemployment" in lowered or "labor" in lowered:
        selected.append("UNRATE")
    if "gdp" in lowered or "growth" in lowered:
        selected.append("GDP")
    if "treasury" in lowered or "yield" in lowered or "valuation" in lowered:
        selected.append("DGS10")
    return selected or ["FEDFUNDS", "CPIAUCSL", "UNRATE"]


def _fred_get_json(url: str, params: dict[str, str | None]) -> dict[str, Any]:
    query = urlencode({key: value for key, value in params.items() if value is not None})
    request_url = f"{url}?{query}"
    last_error: Exception | None = None
    for attempt in range(FRED_MAX_RETRIES):
        try:
            with urlopen(request_url, timeout=FRED_TIMEOUT_SECONDS) as response:
                import json

                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            last_error = exc
            if exc.code not in FRED_RETRY_STATUS_CODES:
                break
        except (TimeoutError, URLError) as exc:
            last_error = exc
        if attempt < FRED_MAX_RETRIES - 1:
            time.sleep(0.25 * (attempt + 1))
    raise RuntimeError(f"FRED request failed: {last_error}") from last_error


def _normalize_series_id(series_id: str) -> str:
    normalized = series_id.strip().upper()
    if normalized not in MACRO_SERIES:
        raise RuntimeError(f"Unsupported macro series '{series_id}'. Supported series: {', '.join(MACRO_SERIES)}.")
    return normalized


def _sample_series(series_id: str, limit: int, cache_status: str) -> MacroSeriesData:
    metadata = MACRO_SERIES[series_id]
    observations = SAMPLE_OBSERVATIONS[series_id][-limit:]
    return MacroSeriesData(
        series_id=series_id,
        title=metadata["title"],
        units=metadata["units"],
        observations=observations,
        source="FRED sample",
        cache_status=cache_status,
    )


def _load_cached_series(series_id: str, limit: int) -> MacroSeriesData | None:
    if not initialize_database():
        return None
    session_factory = get_session_factory()
    if session_factory is None:
        return None

    try:
        with session_factory() as session:
            records = (
                session.query(MacroObservationRecord)
                .filter(MacroObservationRecord.series_id == series_id)
                .order_by(MacroObservationRecord.date.desc())
                .limit(limit)
                .all()
            )
    except Exception:
        return None

    if not records:
        return None
    records.reverse()
    metadata = MACRO_SERIES[series_id]
    return MacroSeriesData(
        series_id=series_id,
        title=metadata["title"],
        units=metadata["units"],
        observations=[{"date": record.date, "value": record.value} for record in records],
        source=records[-1].source,
        cache_status="cache-hit",
    )


def _save_macro_observations(data: MacroSeriesData) -> bool:
    if not initialize_database():
        return False
    session_factory = get_session_factory()
    if session_factory is None:
        return False

    try:
        with session_factory() as session:
            session.query(MacroObservationRecord).filter(MacroObservationRecord.series_id == data.series_id).delete()
            for observation in data.observations:
                session.add(
                    MacroObservationRecord(
                        series_id=data.series_id,
                        date=str(observation["date"]),
                        value=float(observation["value"]),
                        source=data.source,
                        fetched_at=datetime.now(timezone.utc),
                    )
                )
            session.commit()
    except Exception:
        return False
    return True


def _series_response(data: MacroSeriesData) -> MacroSeriesResponse:
    return MacroSeriesResponse(
        series_id=data.series_id,
        title=data.title,
        units=data.units,
        source=data.source,
        observations=data.observations,
        summary=_series_summary_line(
            MacroSeriesResponse(
                series_id=data.series_id,
                title=data.title,
                units=data.units,
                source=data.source,
                observations=data.observations,
                cache_status=data.cache_status,
                message="",
            )
        ),
        cache_status=data.cache_status,
        message=f"Macro series {data.series_id} loaded from {data.cache_status}.",
    )


def _series_summary_line(item: MacroSeriesResponse) -> str:
    if not item.observations:
        return f"{item.series_id}: no observations available."
    latest = item.observations[-1]
    trend = _trend_label(item.observations)
    return (
        f"{item.title or item.series_id} ({item.series_id}) latest value is {latest['value']} "
        f"on {latest['date']} ({item.units}); recent trend is {trend}."
    )


def _trend_label(observations: list[dict[str, str | float]]) -> str:
    if len(observations) < 2:
        return "flat/insufficient history"
    first = float(observations[0]["value"])
    latest = float(observations[-1]["value"])
    delta = latest - first
    if abs(delta) < 0.01:
        return "flat"
    return "up" if delta > 0 else "down"


def _macro_linkage_text(question: str) -> str:
    lowered = question.lower()
    company_context = "company financial risk"
    if "apple" in lowered or "aapl" in lowered:
        company_context = "Apple risk"
    if "valuation" in lowered or "rate" in lowered or "interest" in lowered:
        return f"Higher rates can pressure {company_context} through discount rates, financing costs, demand sensitivity, and investor risk appetite."
    if "inflation" in lowered or "cpi" in lowered:
        return f"Inflation can affect {company_context} through input costs, consumer purchasing power, pricing strategy, and margin pressure."
    if "unemployment" in lowered:
        return f"Labor-market weakness can affect {company_context} through consumer demand, credit conditions, and recession sensitivity."
    return f"Macro indicators should be interpreted as context for {company_context}, not as standalone proof of company-specific outcomes."


def _dedupe_series(series_ids: list[str]) -> list[str]:
    selected: list[str] = []
    for series_id in series_ids:
        normalized = _normalize_series_id(series_id)
        if normalized not in selected:
            selected.append(normalized)
    return selected


def _parse_float(value: Any) -> float | None:
    try:
        if value in {None, "."}:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None
