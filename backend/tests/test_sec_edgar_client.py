from pathlib import Path

import pytest

from app.services import sec_edgar_client
from app.services.sec_edgar_client import SecEdgarError, clean_filing_text, fetch_latest_filing


def test_clean_filing_text_removes_html_and_scripts() -> None:
    raw = "<html><script>ignore()</script><body><h1>Item 1A. Risk Factors</h1><p>Revenue risk&nbsp;exists.</p></body></html>"

    cleaned = clean_filing_text(raw)

    assert "ignore" not in cleaned
    assert "Risk Factors" in cleaned
    assert "Revenue risk exists." in cleaned


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


def test_fetch_latest_filing_requires_known_ticker(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sec_edgar_client, "_get_json", lambda url: {})

    with pytest.raises(SecEdgarError, match="Ticker was not found"):
        fetch_latest_filing(ticker="NOPE", cik=None, form_type="10-K")
