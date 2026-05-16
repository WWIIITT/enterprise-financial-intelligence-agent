from app.agents.orchestrator import build_orchestrated_chat_response, route_question
from app.api.schemas import ChatRequest


def test_router_selects_policy_route() -> None:
    assert route_question("What does the AI Usage Policy say about approved use?") == "policy"


def test_router_selects_document_route() -> None:
    assert route_question("What risks are mentioned for Apple?") == "document"


def test_router_selects_macro_route() -> None:
    assert route_question("How is inflation trending based on CPI?") == "macro"


def test_router_selects_macro_document_route() -> None:
    assert route_question("How do interest rates affect Apple valuation risk?") == "macro_document"


def test_router_selects_sql_route() -> None:
    assert route_question("Show Apple revenue trend from structured financial data") == "sql"


def test_macro_response_uses_langgraph_trace(monkeypatch) -> None:
    monkeypatch.setattr("app.services.macro_service.initialize_database", lambda: False)

    response = build_orchestrated_chat_response(ChatRequest(message="How is inflation trending based on CPI?"))

    assert response.agent == "macro-analysis-agent"
    assert any(step.step == "route" for step in response.trace)
    assert any(step.step == "macro_analysis" for step in response.trace)
    assert response.sources[0].source_type == "macro"


def test_fallback_response_uses_langgraph_trace() -> None:
    response = build_orchestrated_chat_response(ChatRequest(message="Explain unrelated quantum battery patents in detail."))

    assert any(step.step == "route" for step in response.trace)
    assert response.agent in {"rag-orchestrator-empty-index", "rag-orchestrator-low-confidence", "rag-orchestrator"}


def test_sql_response_uses_langgraph_trace(monkeypatch) -> None:
    monkeypatch.setattr("app.services.sql_analytics_service.initialize_database", lambda: False)

    response = build_orchestrated_chat_response(ChatRequest(message="Show Apple revenue trend from structured financial data"))

    assert response.agent == "sql-analytics-agent"
    assert any(step.step == "route" for step in response.trace)
    assert any(step.step == "sql_analytics" for step in response.trace)
    assert response.sources[0].source_type == "sql"
