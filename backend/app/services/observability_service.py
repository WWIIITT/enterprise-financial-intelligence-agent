from __future__ import annotations

from collections import Counter
from typing import Iterable

from sqlalchemy import select

from app.api.schemas import (
    LatestEvaluationSummary,
    ObservabilityDistributionItem,
    ObservabilitySummaryResponse,
    RecentRequestSummary,
    RecentSecurityEvent,
)
from app.core.database import get_session_factory, initialize_database
from app.models import EvaluationRunRecord, RequestLogRecord, SecurityAuditRecord


def get_observability_summary(limit: int = 10) -> ObservabilitySummaryResponse:
    if not initialize_database():
        return _empty_summary()

    session_factory = get_session_factory()
    if session_factory is None:
        return _empty_summary()

    try:
        with session_factory() as session:
            request_logs = list(
                session.scalars(
                    select(RequestLogRecord).order_by(RequestLogRecord.created_at.desc()).limit(500)
                )
            )
            evaluation_runs = list(
                session.scalars(
                    select(EvaluationRunRecord).order_by(EvaluationRunRecord.created_at.desc()).limit(20)
                )
            )
            security_audits = list(
                session.scalars(
                    select(SecurityAuditRecord).order_by(SecurityAuditRecord.created_at.desc()).limit(500)
                )
            )
    except Exception:
        return _empty_summary()

    latencies = sorted(log.latency_ms for log in request_logs)
    request_count = len(request_logs)
    return ObservabilitySummaryResponse(
        status="completed",
        request_count=request_count,
        latency_avg_ms=round(sum(latencies) / request_count, 2) if request_count else 0,
        latency_p95_ms=_percentile(latencies, 0.95),
        average_sources=round(sum(log.sources_count for log in request_logs) / request_count, 2) if request_count else 0,
        estimated_total_cost_usd=round(sum(log.estimated_cost_usd for log in request_logs), 6),
        agent_routes=_distribution(log.selected_agent for log in request_logs),
        recent_requests=[
            RecentRequestSummary(
                selected_agent=log.selected_agent,
                sources_count=log.sources_count,
                latency_ms=log.latency_ms,
                estimated_cost_usd=log.estimated_cost_usd,
                created_at=log.created_at.isoformat(),
            )
            for log in request_logs[:limit]
        ],
        latest_evaluation=_latest_evaluation(evaluation_runs),
        security_actions=_distribution(audit.action for audit in security_audits),
        recent_security_events=[
            RecentSecurityEvent(
                risk_level=audit.risk_level,
                action=audit.action,
                finding_count=audit.finding_count,
                agent=audit.agent or "security-governance-agent",
                created_at=audit.created_at.isoformat(),
            )
            for audit in security_audits[:limit]
        ],
    )


def _empty_summary() -> ObservabilitySummaryResponse:
    return ObservabilitySummaryResponse(
        status="completed",
        request_count=0,
        latency_avg_ms=0,
        latency_p95_ms=0,
        average_sources=0,
        estimated_total_cost_usd=0,
        agent_routes=[],
        recent_requests=[],
        latest_evaluation=None,
        security_actions=[],
        recent_security_events=[],
    )


def _distribution(values: Iterable[str]) -> list[ObservabilityDistributionItem]:
    counts = Counter(value for value in values if value)
    total = sum(counts.values())
    return [
        ObservabilityDistributionItem(
            name=name,
            count=count,
            share=round(count / total, 4) if total else 0,
        )
        for name, count in counts.most_common()
    ]


def _latest_evaluation(evaluation_runs: list[EvaluationRunRecord]) -> LatestEvaluationSummary | None:
    if not evaluation_runs:
        return None
    latest = evaluation_runs[0]
    return LatestEvaluationSummary(
        suite=latest.suite,
        cases_total=latest.cases_total,
        cases_passed=latest.cases_passed,
        pass_rate=latest.pass_rate,
        latency_ms=latest.latency_ms,
        created_at=latest.created_at.isoformat(),
    )


def _percentile(values: list[int], percentile: float) -> int:
    if not values:
        return 0
    index = min(len(values) - 1, int(round((len(values) - 1) * percentile)))
    return values[index]
