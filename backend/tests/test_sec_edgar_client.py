from pathlib import Path

import httpx
import pytest

from app.services import sec_edgar_client
from app.services.sec_edgar_client import SecEdgarError, clean_filing_text, fetch_latest_filing, parse_filing_sections


def test_clean_filing_text_removes_html_and_scripts() -> None:
    raw = (
        "<html><script>ignore()</script><body><h1>Item 1A. Risk Factors</h1>"
        "<p>The Companyâ€™s revenue risk&nbsp;exists.</p></body></html>"
    )

    cleaned = clean_filing_text(raw)

    assert "ignore" not in cleaned
    assert "Risk Factors" in cleaned
    assert "The Company's revenue risk exists." in cleaned


def test_fetch_latest_filing_uses_ticker_mapping_and_recent_filing(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(sec_edgar_client, "RAW_SEC_DIR", tmp_path)
    monkeypatch.setattr(sec_edgar_client.settings, "sec_user_agent", "test user test@example.com")

    def fake_get_json(url: str) -> dict:
        if url == sec_edgar_client.SEC_TICKER_URL:
            return {"0": {"cik_str": 320193, "ticker": "AAPL", "title": "Apple Inc."}}
        if url == sec_edgar_client.SEC_SUBMISSIONS_URL.format(cik="0000320193"):
            return {
                "filings": {
                    "recent": {
                        "form": ["8-K", "10-K"],
                        "accessionNumber": ["0000320193-24-000001", "0000320193-24-000123"],
                        "filingDate": ["2024-01-01", "2024-11-01"],
                        "primaryDocument": ["aapl-8k.htm", "aapl-20240928.htm"],
                    }
                }
            }
        raise AssertionError(f"unexpected URL: {url}")

    def fake_get_text(url: str) -> str:
        assert url == "https://www.sec.gov/Archives/edgar/data/320193/000032019324000123/aapl-20240928.htm"
        return "<html><body>Item 1A. Risk Factors Apple revenue risk and supply chain constraints.</body></html>"

    monkeypatch.setattr(sec_edgar_client, "_get_json", fake_get_json)
    monkeypatch.setattr(sec_edgar_client, "_get_text", fake_get_text)

    filing = fetch_latest_filing(ticker="AAPL", cik=None, form_type="10-K")

    assert filing.ticker == "AAPL"
    assert filing.cik == "0000320193"
    assert filing.form_type == "10-K"
    assert filing.accession_number == "0000320193-24-000123"
    assert filing.filing_date == "2024-11-01"
    assert "Apple revenue risk" in filing.text
    assert filing.raw_path.exists()


def test_fetch_latest_filing_selects_by_year_and_accession(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(sec_edgar_client, "RAW_SEC_DIR", tmp_path)
    monkeypatch.setattr(sec_edgar_client.settings, "sec_user_agent", "test user test@example.com")

    def fake_get_json(url: str) -> dict:
        if url == sec_edgar_client.SEC_TICKER_URL:
            return {"0": {"cik_str": 320193, "ticker": "AAPL", "title": "Apple Inc."}}
        return {
            "filings": {
                "recent": {
                    "form": ["10-K", "10-K", "10-Q"],
                    "accessionNumber": ["0000320193-25-000079", "0000320193-24-000123", "0000320193-25-000050"],
                    "filingDate": ["2025-10-31", "2024-11-01", "2025-05-01"],
                    "primaryDocument": ["aapl-20250927.htm", "aapl-20240928.htm", "aapl-20250329.htm"],
                }
            }
        }

    monkeypatch.setattr(sec_edgar_client, "_get_json", fake_get_json)
    monkeypatch.setattr(sec_edgar_client, "_get_text", lambda url: "<html><body>Item 1A. Risk Factors Apple risk.</body></html>")

    by_year = fetch_latest_filing(ticker="AAPL", cik=None, form_type="10-K", filing_year=2024)
    by_accession = fetch_latest_filing(
        ticker="AAPL",
        cik=None,
        form_type="10-K",
        accession_number="0000320193-25-000079",
    )

    assert by_year.accession_number == "0000320193-24-000123"
    assert by_accession.filing_date == "2025-10-31"


def test_fetch_latest_filing_requires_known_ticker(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sec_edgar_client, "_get_json", lambda url: {})

    with pytest.raises(SecEdgarError, match="Ticker was not found"):
        fetch_latest_filing(ticker="NOPE", cik=None, form_type="10-K")


def test_parse_filing_sections_assigns_sec_items() -> None:
    sections = parse_filing_sections(
        "Cover page. Item 1. Business Apple sells products. "
        "Item 1A. Risk Factors Apple faces supply risk. "
        "Item 7. Management's Discussion and Analysis Revenue discussion. "
        "Item 7A. Quantitative and Qualitative Disclosures About Market Risk FX risk."
    )

    assert [section.name for section in sections] == ["Filing", "Business", "Risk Factors", "MD&A", "Market Risk"]


def test_sec_request_retries_temporary_failures(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = {"count": 0}

    class FakeResponse:
        def __init__(self, status_code: int) -> None:
            self.status_code = status_code

        def raise_for_status(self) -> None:
            if self.status_code >= 400:
                raise httpx.HTTPStatusError("failed", request=httpx.Request("GET", "https://example.com"), response=httpx.Response(self.status_code))

    class FakeClient:
        def get(self, url: str) -> FakeResponse:
            calls["count"] += 1
            return FakeResponse(503 if calls["count"] == 1 else 200)

    monkeypatch.setattr(sec_edgar_client.time, "sleep", lambda seconds: None)

    response = sec_edgar_client._request_with_retry(FakeClient(), "https://example.com")

    assert response.status_code == 200
    assert calls["count"] == 2
