from fastapi.testclient import TestClient

from app.api.schemas import SqlAnalyzeRequest
from app.main import app
from app.services.sql_analytics_service import (
    analyze_financial_facts,
    normalize_metric,
    parse_company_facts_payload,
    sample_company_facts,
)


client = TestClient(app)


def test_sample_company_facts_returns_aapl_facts() -> None:
    payload = sample_company_facts("AAPL")

    assert payload.ticker == "AAPL"
    assert payload.facts
    assert any(fact.concept == "Revenues" for fact in payload.facts)


def test_company_facts_parser_reads_sec_style_payload() -> None:
    payload = {
        "entityName": "Apple Inc.",
        "facts": {
            "us-gaap": {
                "Revenues": {
                    "label": "Revenue",
                    "units": {
                        "USD": [
                            {
                                "fy": 2024,
                                "fp": "FY",
                                "form": "10-K",
                                "filed": "2024-11-01",
                                "val": 391035000000,
                                "accn": "0000320193-24-000123",
                            }
                        ]
                    },
                }
            }
        },
    }

    parsed = parse_company_facts_payload("AAPL", "0000320193", payload)

    assert parsed.company_name == "Apple Inc."
    assert parsed.facts[0].value == 391035000000
    assert parsed.facts[0].concept == "Revenues"


def test_sql_analysis_returns_sample_revenue(monkeypatch) -> None:
    monkeypatch.setattr("app.services.sql_analytics_service.initialize_database", lambda: False)

    response = analyze_financial_facts(SqlAnalyzeRequest(ticker="AAPL", metric="revenue", period="annual", limit=3))

    assert response.agent == "sql-analytics-agent"
    assert len(response.facts) == 3
    assert "Revenue" in response.answer
    assert response.sources[0].source_type == "sql"


def test_unsupported_metric_rejected() -> None:
    try:
        normalize_metric("drop table users")
    except RuntimeError as exc:
        assert "Unsupported SQL metric" in str(exc)
    else:
        raise AssertionError("unsupported metric should fail")


def test_sql_analyze_endpoint_shape(monkeypatch) -> None:
    monkeypatch.setattr("app.services.sql_analytics_service.initialize_database", lambda: False)

    response = client.post("/api/sql/analyze", json={"ticker": "AAPL", "metric": "revenue", "period": "annual", "limit": 3})
    body = response.json()

    assert response.status_code == 200
    assert body["agent"] == "sql-analytics-agent"
    assert body["facts"]
    assert body["sources"]
