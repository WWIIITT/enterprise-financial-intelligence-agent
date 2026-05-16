from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.main import app
from app.models import EvaluationRunRecord, RequestLogRecord, SecurityAuditRecord
from app.services.observability_service import get_observability_summary


client = TestClient(app)


def test_observability_summary_empty_when_db_unavailable(monkeypatch) -> None:
    monkeypatch.setattr("app.services.observability_service.initialize_database", lambda: False)

    summary = get_observability_summary()

    assert summary.status == "completed"
    assert summary.request_count == 0
    assert summary.agent_routes == []


def test_observability_summary_aggregates_records(monkeypatch) -> None:
    class FakeSession:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, traceback):
            return False

        def scalars(self, statement):
            statement_text = str(statement)
            if "request_logs" in statement_text:
                records = [
                    RequestLogRecord(
                        message="one",
                        selected_agent="document-research-agent",
                        sources_count=3,
                        latency_ms=100,
                        estimated_cost_usd=0.01,
                    ),
                    RequestLogRecord(
                        message="two",
                        selected_agent="macro-analysis-agent",
                        sources_count=1,
                        latency_ms=300,
                        estimated_cost_usd=0.02,
                    ),
                ]
                for record in records:
                    record.created_at = now
                return records
            if "evaluation_runs" in statement_text:
                records = [
                    EvaluationRunRecord(
                        suite="all",
                        cases_total=10,
                        cases_passed=9,
                        pass_rate=0.9,
                        latency_ms=900,
                    )
                ]
                for record in records:
                    record.created_at = now
                return records
            if "security_audits" in statement_text:
                records = [
                    SecurityAuditRecord(
                        message_hash="abc",
                        role="research_analyst",
                        risk_level="medium",
                        action="mask",
                        finding_count=1,
                    )
                ]
                for record in records:
                    record.created_at = now
                return records
            return []

    now = datetime.now(timezone.utc)
    monkeypatch.setattr("app.services.observability_service.initialize_database", lambda: True)
    monkeypatch.setattr("app.services.observability_service.get_session_factory", lambda: lambda: FakeSession())

    summary = get_observability_summary()

    assert summary.request_count == 2
    assert summary.latency_avg_ms == 200
    assert summary.latency_p95_ms == 300
    assert summary.average_sources == 2
    assert summary.estimated_total_cost_usd == 0.03
    assert summary.agent_routes[0].name == "document-research-agent"
    assert summary.latest_evaluation is not None
    assert summary.latest_evaluation.suite == "all"
    assert summary.security_actions[0].name == "mask"


def test_observability_endpoint_returns_schema() -> None:
    response = client.get("/api/observability/summary")
    body = response.json()

    assert response.status_code == 200
    assert body["status"] == "completed"
    assert "request_count" in body
    assert "agent_routes" in body
    assert "security_actions" in body
