from app.api.schemas import ChatRequest, MacroAnalyzeRequest
from app.services.macro_service import FredClient, analyze_macro_context, get_macro_series
from app.services.rag_service import build_rag_chat_response


def test_fred_client_uses_sample_fallback_without_key() -> None:
    client = FredClient(api_key="")

    series = client.fetch_series("FEDFUNDS", limit=2)

    assert series.series_id == "FEDFUNDS"
    assert series.cache_status == "sample-fallback"
    assert len(series.observations) == 2


def test_macro_series_response_shape(monkeypatch) -> None:
    monkeypatch.setattr("app.services.macro_service.initialize_database", lambda: False)

    response = get_macro_series("CPIAUCSL", limit=2, client=FredClient(api_key=""))

    assert response.series_id == "CPIAUCSL"
    assert response.title
    assert response.units
    assert response.observations
    assert response.summary
    assert response.cache_status == "sample-fallback"


def test_macro_analysis_response() -> None:
    response = analyze_macro_context(
        MacroAnalyzeRequest(
            series_ids=["FEDFUNDS", "CPIAUCSL"],
            question="How do current rates and inflation affect Apple risk?",
            limit=2,
        )
    )

    assert response.agent == "macro-analysis-agent"
    assert len(response.series) == 2
    assert "## Macro Context" in response.answer
    assert any(source.source_type == "macro" for source in response.sources)


def test_macro_chat_routes_to_macro_agent(monkeypatch) -> None:
    monkeypatch.setattr("app.services.macro_service.initialize_database", lambda: False)

    response = build_rag_chat_response(ChatRequest(message="How is inflation trending based on CPI?"))

    assert response.agent == "macro-analysis-agent"
    assert "CPIAUCSL" in response.answer
    assert response.sources[0].source_type == "macro"


def test_company_macro_chat_can_include_sec_context(monkeypatch) -> None:
    monkeypatch.setattr("app.services.macro_service.initialize_database", lambda: False)

    response = build_rag_chat_response(ChatRequest(message="How do interest rates affect Apple valuation risk?"))

    assert response.agent in {"macro-analysis-agent", "macro-document-orchestrator"}
    assert "Company Risk Linkage" in response.answer
    assert any(source.source_type == "macro" for source in response.sources)
