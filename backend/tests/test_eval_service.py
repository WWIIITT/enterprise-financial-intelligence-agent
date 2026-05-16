from app.services.eval_service import run_evaluation_suite
from app.api.schemas import EvalRunRequest


def test_eval_suite_returns_metrics(monkeypatch) -> None:
    class FakeSource:
        source_type = "sec"
        citation = "AAPL 10-K 2025-10-31 0000320193-25-000079 Risk Factors chunk 1"

    class FakeResponse:
        answer = "## Key Risks\n- risk\n## Sources"
        agent = "document-research-agent"
        sources = [FakeSource()]

    monkeypatch.setattr("app.services.eval_service.build_orchestrated_chat_response", lambda request: FakeResponse())

    result = run_evaluation_suite(EvalRunRequest(suite="sec-smoke"))

    assert result["status"] == "completed"
    assert result["metrics"]["cases_total"] >= 1
    assert result["metrics"]["pass_rate"] > 0


def test_macro_eval_suite_returns_metrics(monkeypatch) -> None:
    class FakeSource:
        source_type = "macro"
        citation = "FRED CPIAUCSL"

    class FakeResponse:
        answer = "## Macro Context\n- CPIAUCSL inflation trend\n## Sources"
        agent = "macro-analysis-agent"
        sources = [FakeSource()]

    monkeypatch.setattr("app.services.eval_service.build_orchestrated_chat_response", lambda request: FakeResponse())

    result = run_evaluation_suite(EvalRunRequest(suite="macro-smoke"))

    assert result["status"] == "completed"
    assert result["metrics"]["cases_total"] >= 1
