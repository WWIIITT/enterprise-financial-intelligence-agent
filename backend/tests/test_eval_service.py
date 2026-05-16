from app.api.schemas import EvalRunRequest, Metrics, TraceStep
from app.services.eval_service import generate_evaluation_report, run_evaluation_suite


class FakeSource:
    def __init__(self, source_type: str, citation: str) -> None:
        self.source_type = source_type
        self.citation = citation


class FakeResponse:
    def __init__(self, answer: str, agent: str, source_type: str, citation: str) -> None:
        self.answer = answer
        self.agent = agent
        self.sources = [FakeSource(source_type, citation)]
        self.trace = [TraceStep(step="receive", detail="ok"), TraceStep(step="route", detail="ok")]
        self.metrics = Metrics(latency_ms=12)


def test_eval_suite_returns_expanded_metrics(monkeypatch) -> None:
    response = FakeResponse(
        answer="## Key Risks\n- risk\n## Sources\n0000320193-25-000079",
        agent="document-research-agent",
        source_type="sec",
        citation="AAPL 10-K 2025-10-31 0000320193-25-000079 Risk Factors chunk 1",
    )
    monkeypatch.setattr("app.services.eval_service.build_orchestrated_chat_response", lambda request: response)
    monkeypatch.setattr("app.services.eval_service._record_evaluation_run", lambda suite, metrics: True)

    result = run_evaluation_suite(EvalRunRequest(suite="sec-smoke"))

    assert result["status"] == "completed"
    assert result["metrics"]["cases_total"] >= 1
    assert "route_accuracy" in result["metrics"]
    assert "citation_score" in result["metrics"]
    assert "latency_p95_ms" in result["metrics"]


def test_macro_eval_suite_returns_metrics(monkeypatch) -> None:
    response = FakeResponse(
        answer="## Macro Context\n- CPIAUCSL inflation trend\n## Sources",
        agent="macro-analysis-agent",
        source_type="macro",
        citation="FRED CPIAUCSL",
    )
    monkeypatch.setattr("app.services.eval_service.build_orchestrated_chat_response", lambda request: response)
    monkeypatch.setattr("app.services.eval_service._record_evaluation_run", lambda suite, metrics: True)

    result = run_evaluation_suite(EvalRunRequest(suite="macro-smoke"))

    assert result["status"] == "completed"
    assert result["metrics"]["cases_total"] >= 1


def test_forbidden_terms_flag_hallucination_risk(monkeypatch) -> None:
    response = FakeResponse(
        answer="This answer contains invented unsupported data.",
        agent="macro-analysis-agent",
        source_type="macro",
        citation="FRED CPIAUCSL",
    )
    monkeypatch.setattr("app.services.eval_service.build_orchestrated_chat_response", lambda request: response)
    monkeypatch.setattr("app.services.eval_service._load_cases", lambda suite: [{
        "id": "forbidden",
        "suite": "unit",
        "question": "test",
        "forbidden_answer_terms": ["invented"],
    }])
    monkeypatch.setattr("app.services.eval_service._record_evaluation_run", lambda suite, metrics: True)

    result = run_evaluation_suite(EvalRunRequest(suite="unit"))

    assert result["metrics"]["hallucination_risk_count"] == 1
    assert not result["results"][0]["passed"]


def test_generate_report_returns_markdown(monkeypatch) -> None:
    response = FakeResponse(
        answer="## Macro Context\n- CPIAUCSL inflation trend\n## Sources",
        agent="macro-analysis-agent",
        source_type="macro",
        citation="FRED CPIAUCSL",
    )
    monkeypatch.setattr("app.services.eval_service.build_orchestrated_chat_response", lambda request: response)
    monkeypatch.setattr("app.services.eval_service._record_evaluation_run", lambda suite, metrics: True)
    monkeypatch.setattr("app.services.eval_service._write_report_files", lambda result, markdown: {"markdown": "", "json": ""})

    report = generate_evaluation_report(EvalRunRequest(suite="macro-smoke"))

    assert report["status"] == "completed"
    assert "# Evaluation Report" in report["markdown"]
    assert "pass_rate" in report["summary"]
