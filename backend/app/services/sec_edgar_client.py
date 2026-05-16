from __future__ import annotations

import html
import re
from dataclasses import dataclass
from pathlib import Path

import httpx

from app.core.config import ROOT_DIR, settings


SEC_TICKER_URL = "https://www.sec.gov/files/company_tickers.json"
SEC_SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
SEC_ARCHIVES_URL = "https://www.sec.gov/Archives/edgar/data/{cik}/{accession}/{document}"
RAW_SEC_DIR = ROOT_DIR / "data" / "raw" / "sec"


class SecEdgarError(RuntimeError):
    pass


@dataclass(frozen=True)
class SecFilingDocument:
    ticker: str
    cik: str
    company_name: str
    form_type: str
    accession_number: str
    filing_date: str
    primary_document: str
    document_url: str
    text: str
    raw_path: Path

    @property
    def citation_prefix(self) -> str:
        return f"{self.ticker} {self.form_type} {self.filing_date} {self.accession_number}"


def fetch_latest_filing(ticker: str | None, cik: str | None, form_type: str = "10-K") -> SecFilingDocument:
    normalized_form = form_type.upper()
    resolved_cik, resolved_ticker, company_name = _resolve_company(ticker, cik)
    submissions = _get_json(SEC_SUBMISSIONS_URL.format(cik=resolved_cik))
    recent = submissions.get("filings", {}).get("recent", {})
    filing = _select_recent_filing(recent, normalized_form)
    accession_number = filing["accessionNumber"]
    primary_document = filing["primaryDocument"]
    archive_cik = str(int(resolved_cik))
    archive_accession = accession_number.replace("-", "")
    document_url = SEC_ARCHIVES_URL.format(
        cik=archive_cik,
        accession=archive_accession,
        document=primary_document,
    )
    raw_content = _get_text(document_url)
    cleaned_text = clean_filing_text(raw_content)
    if not cleaned_text:
        raise SecEdgarError(f"SEC filing document was empty after parsing: {document_url}")

    raw_path = _write_raw_filing(
        ticker=resolved_ticker,
        form_type=filing["form"],
        accession_number=accession_number,
        primary_document=primary_document,
        raw_content=raw_content,
    )
    return SecFilingDocument(
        ticker=resolved_ticker,
        cik=resolved_cik,
        company_name=company_name,
        form_type=filing["form"],
        accession_number=accession_number,
        filing_date=filing["filingDate"],
        primary_document=primary_document,
        document_url=document_url,
        text=cleaned_text,
        raw_path=raw_path,
    )


def clean_filing_text(raw_content: str) -> str:
    without_scripts = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", raw_content)
    without_tags = re.sub(r"(?s)<[^>]+>", " ", without_scripts)
    decoded = html.unescape(without_tags)
    decoded = re.sub(r"\s+", " ", decoded)
    return decoded.strip()


def _resolve_company(ticker: str | None, cik: str | None) -> tuple[str, str, str]:
    if cik:
        normalized_cik = _normalize_cik(cik)
        return normalized_cik, (ticker or normalized_cik).upper(), ticker.upper() if ticker else normalized_cik
    if not ticker:
        raise SecEdgarError("Live SEC ingestion requires either ticker or cik.")

    ticker_map = _get_json(SEC_TICKER_URL)
    normalized_ticker = ticker.upper()
    for record in ticker_map.values():
        if str(record.get("ticker", "")).upper() == normalized_ticker:
            return _normalize_cik(str(record["cik_str"])), normalized_ticker, str(record.get("title", normalized_ticker))
    raise SecEdgarError(f"Ticker was not found in SEC ticker mapping: {ticker}")


def _select_recent_filing(recent: dict[str, list], form_type: str) -> dict[str, str]:
    forms = recent.get("form", [])
    accession_numbers = recent.get("accessionNumber", [])
    filing_dates = recent.get("filingDate", [])
    primary_documents = recent.get("primaryDocument", [])

    for index, form in enumerate(forms):
        if str(form).upper() != form_type:
            continue
        try:
            return {
                "form": str(forms[index]),
                "accessionNumber": str(accession_numbers[index]),
                "filingDate": str(filing_dates[index]),
                "primaryDocument": str(primary_documents[index]),
            }
        except IndexError as exc:
            raise SecEdgarError("SEC submissions response has inconsistent filing metadata arrays.") from exc

    raise SecEdgarError(f"No recent {form_type} filing found in SEC submissions response.")


def _normalize_cik(cik: str) -> str:
    digits = re.sub(r"\D", "", cik)
    if not digits:
        raise SecEdgarError(f"Invalid CIK: {cik}")
    return digits.zfill(10)


def _get_json(url: str) -> dict:
    with _client() as client:
        response = client.get(url)
        response.raise_for_status()
        return response.json()


def _get_text(url: str) -> str:
    with _client() as client:
        response = client.get(url)
        response.raise_for_status()
        return response.text


def _client() -> httpx.Client:
    if not settings.sec_user_agent:
        raise SecEdgarError("SEC_USER_AGENT is required for live SEC EDGAR ingestion.")
    return httpx.Client(
        headers={
            "User-Agent": settings.sec_user_agent,
            "Accept-Encoding": "gzip, deflate",
            "Accept": "application/json,text/html,text/plain,*/*",
        },
        timeout=20,
        follow_redirects=True,
    )


def _write_raw_filing(
    ticker: str,
    form_type: str,
    accession_number: str,
    primary_document: str,
    raw_content: str,
) -> Path:
    RAW_SEC_DIR.mkdir(parents=True, exist_ok=True)
    safe_document = re.sub(r"[^a-zA-Z0-9_.-]+", "_", primary_document)
    filename = f"{ticker.upper()}_{form_type.replace('/', '-')}_{accession_number}_{safe_document}"
    path = RAW_SEC_DIR / filename
    path.write_text(raw_content, encoding="utf-8")
    return path
