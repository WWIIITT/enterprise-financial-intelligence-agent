from __future__ import annotations

import json
from pathlib import Path
from time import perf_counter
from typing import Any

from app.agents.orchestrator import build_orchestrated_chat_response
from app.api.schemas import ChatRequest, EvalRunRequest
from app.core.config import ROOT_DIR
from app.core.database import get_session_factory, initialize_database
from app.models import EvaluationRunRecord


SEC_CASES_PATH = ROOT_DIR / "backend" / "app" / "evals" / "sec_filing_cases.json"
MACRO_CASES_PATH = ROOT_DIR / "backend" / "app" / "evals" / "macro_cases.json"
ORCHESTRATOR_CASES_PATH = ROOT_DIR / "backend" / "app" / "evals" / "orchestrator_cases.json"
SQL_CASES_PATH = ROOT_DIR / "backend" / "app" / "evals" / "sql_cases.json"
REPORT_DIR = ROOT_DIR / "data" / "reports"
REPORT_MD_PATH = REPORT_DIR / "evaluation-report.md"
REPORT_JSON_PATH = REPORT_DIR / "evaluation-report.json"


def run_evaluation_suite(request: EvalRunRequest) -> dict[str, object]:
    cases = _load_cases(request.suite)
    started = perf_counter()
    results = [_run_case(case) for case in cases]
    latency_ms = int((perf_counter() - started) * 1000)
    metrics = _aggregate_metrics(results, latency_ms)
    _record_evaluation_run(request.suite, metrics)
    return {
        "status": "completed",
        "suite": request.suite,
        "metrics": metrics,
        "results": results,
        "message": "Evaluation suite completed with deterministic route, citation, source, and answer checks.",
    }


def generate_evaluation_report(request: EvalRunRequest) -> dict[str, object]:
    result = run_evaluation_suite(request)
    markdown = _build_markdown_report(result)
    report_paths = _write_report_files(result, markdown)
    return {
        "status": "completed",
        "suite": request.suite,
        "summary": result["metrics"],
        "markdown": markdown,
        "report_paths": report_paths,
    }


def _load_cases(suite: str) -> list[dict[str, Any]]:
    paths = [SEC_CASES_PATH]
    if MACRO_CASES_PATH.exists():
        paths.append(MACRO_CASES_PATH)
    if ORCHESTRATOR_CASES_PATH.exists():
        paths.append(ORCHESTRATOR_CASES_PATH)
    if SQL_CASES_PATH.exists():
        paths.append(SQL_CASES_PATH)

    cases: list[dict[str, Any]] = []
    for path in paths:
        with path.open(encoding="utf-8") as handle:
            cases.extend(json.load(handle))
    selected = [case for case in cases if suite in {"all", case.get("suite")}]
    return selected or cases


def _run_case(case: dict[str, Any]) -> dict[str, object]:
    started = perf_counter()
    response = build_orchestrated_chat_response(ChatRequest(message=case["question"]))
    latency_ms = int((perf_counter() - started) * 1000)
    failures: list[str] = []
    scores = {
        "route": _score_route(case, response, failures),
        "source": _score_source_coverage(case, response, failures),
        "citation": _score_citations(case, response, failures),
        "answer_terms": _score_answer_terms(case, response, failures),
        "latency": _score_latency(case, latency_ms, failures),
        "trace": _score_trace(case, response, failures),
    }
    hallucination_risk = _apply_forbidden_terms(case, response, failures)

    return {
        "id": case["id"],
        "category": case.get("category", case.get("suite", "uncategorized")),
        "passed": not failures,
        "failures": failures,
        "agent": response.agent,
        "sources_count": len(response.sources),
        "latency_ms": latency_ms,
        "scores": scores,
        "trace_steps": [step.step for step in response.trace],
        "hallucination_risk": hallucination_risk,
    }


def _score_route(case: dict[str, Any], response, failures: list[str]) -> float | None:
    expected_agent = case.get("expected_agent")
    if not expected_agent:
        return None
    if response.agent != expected_agent:
        failures.append(f"expected agent {expected_agent}, got {response.agent}")
        return 0.0
    return 1.0


def _score_source_coverage(case: dict[str, Any], response, failures: list[str]) -> float | None:
    score: float | None = None
    required_source_type = case.get("required_source_type")
    if required_source_type:
        score = 1.0 if any(source.source_type == required_source_type for source in response.sources) else 0.0
        if score == 0.0:
            failures.append(f"missing source type {required_source_type}")
    min_sources = case.get("min_sources")
    if min_sources is not None:
        source_score = 1.0 if len(response.sources) >= int(min_sources) else 0.0
        if source_score == 0.0:
            failures.append(f"expected at least {min_sources} source(s), got {len(response.sources)}")
        score = source_score if score is None else min(score, source_score)
    return score


def _score_citations(case: dict[str, Any], response, failures: list[str]) -> float | None:
    required_terms = case.get("required_citation_terms", [])
    if not required_terms:
        return None
    citations = " ".join(str(source.citation or "") for source in response.sources).lower()
    hits = 0
    for term in required_terms:
        if str(term).lower() in citations:
            hits += 1
        else:
            failures.append(f"citation missing term {term}")
    return round(hits / len(required_terms), 4) if required_terms else None


def _score_answer_terms(case: dict[str, Any], response, failures: list[str]) -> float | None:
    required_terms = case.get("required_answer_terms", [])
    if not required_terms:
        return None
    answer_lower = response.answer.lower()
    hits = 0
    for term in required_terms:
        if str(term).lower() in answer_lower:
            hits += 1
        else:
            failures.append(f"answer missing term {term}")
    return round(hits / len(required_terms), 4) if required_terms else None


def _score_latency(case: dict[str, Any], latency_ms: int, failures: list[str]) -> float | None:
    max_latency_ms = case.get("max_latency_ms")
    if max_latency_ms is None:
        return None
    if latency_ms > int(max_latency_ms):
        failures.append(f"latency {latency_ms}ms exceeded {max_latency_ms}ms")
        return 0.0
    return 1.0


def _score_trace(case: dict[str, Any], response, failures: list[str]) -> float | None:
    expected_steps = case.get("expected_trace_steps", [])
    if not expected_steps:
        return None
    trace_steps = {step.step for step in response.trace}
    hits = 0
    for step in expected_steps:
        if step in trace_steps:
            hits += 1
        else:
            failures.append(f"trace missing step {step}")
    return round(hits / len(expected_steps), 4) if expected_steps else None


def _apply_forbidden_terms(case: dict[str, Any], response, failures: list[str]) -> bool:
    answer_lower = response.answer.lower()
    flagged = False
    for term in case.get("forbidden_answer_terms", []):
        if str(term).lower() in answer_lower:
            failures.append(f"forbidden answer term found {term}")
            flagged = True
    return flagged


def _aggregate_metrics(results: list[dict[str, object]], latency_ms: int) -> dict[str, object]:
    total = len(results)
    passed = sum(1 for result in results if result["passed"])
    latencies = sorted(int(result["latency_ms"]) for result in results)
    return {
        "cases_total": total,
        "cases_passed": passed,
        "pass_rate": round(passed / total, 4) if total else 0.0,
        "route_accuracy": _average_score(results, "route"),
        "source_coverage": _average_score(results, "source"),
        "citation_score": _average_score(results, "citation"),
        "answer_term_score": _average_score(results, "answer_terms"),
        "latency_ms": latency_ms,
        "latency_avg_ms": round(sum(latencies) / len(latencies), 2) if latencies else 0,
        "latency_p95_ms": _percentile(latencies, 0.95),
        "hallucination_risk_count": sum(1 for result in results if result["hallucination_risk"]),
    }


def _average_score(results: list[dict[str, object]], key: str) -> float:
    values: list[float] = []
    for result in results:
        score = result["scores"].get(key)  # type: ignore[index]
        if score is not None:
            values.append(float(score))
    return round(sum(values) / len(values), 4) if values else 1.0


def _percentile(values: list[int], percentile: float) -> int:
    if not values:
        return 0
    index = min(len(values) - 1, int(round((len(values) - 1) * percentile)))
    return values[index]


def _build_markdown_report(result: dict[str, object]) -> str:
    metrics = result["metrics"]  # type: ignore[index]
    failed_results = [item for item in result["results"] if not item["passed"]]  # type: ignore[index]
    failed_rows = "\n".join(
        f"| {item['id']} | {item['agent']} | {'; '.join(item['failures'])} |" for item in failed_results
    )
    if not failed_rows:
        failed_rows = "| None | - | - |"
    recommendations = _recommendations(metrics, failed_results)
    return (
        f"# Evaluation Report\n\n"
        f"## Summary\n\n"
        f"- Suite: `{result['suite']}`\n"
        f"- Pass rate: {metrics['pass_rate']}\n"
        f"- Route accuracy: {metrics['route_accuracy']}\n"
        f"- Citation score: {metrics['citation_score']}\n"
        f"- Source coverage: {metrics['source_coverage']}\n"
        f"- Average latency: {metrics['latency_avg_ms']} ms\n"
        f"- P95 latency: {metrics['latency_p95_ms']} ms\n"
        f"- Hallucination risk count: {metrics['hallucination_risk_count']}\n\n"
        f"## Failed Cases\n\n"
        f"| Case | Agent | Failures |\n"
        f"| --- | --- | --- |\n"
        f"{failed_rows}\n\n"
        f"## Recommendations\n\n"
        f"{recommendations}\n"
    )


def _recommendations(metrics: dict[str, object], failed_results: list[dict[str, object]]) -> str:
    recommendations: list[str] = []
    if float(metrics["route_accuracy"]) < 1.0:
        recommendations.append("- Review deterministic router terms for missed intents.")
    if float(metrics["citation_score"]) < 1.0:
        recommendations.append("- Improve citation construction or expected citation terms.")
    if float(metrics["source_coverage"]) < 1.0:
        recommendations.append("- Re-ingest missing source types before running eval.")
    if int(metrics["hallucination_risk_count"]) > 0:
        recommendations.append("- Inspect forbidden term failures and tighten no-answer behavior.")
    if failed_results:
        recommendations.append("- Triage failed cases before expanding the suite.")
    if not recommendations:
        recommendations.append("- No immediate remediation required for this suite.")
    return "\n".join(recommendations)


def _write_report_files(result: dict[str, object], markdown: str) -> dict[str, str]:
    paths = {
        "markdown": str(REPORT_MD_PATH.relative_to(ROOT_DIR)),
        "json": str(REPORT_JSON_PATH.relative_to(ROOT_DIR)),
    }
    try:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        REPORT_MD_PATH.write_text(markdown, encoding="utf-8")
        REPORT_JSON_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    except OSError:
        return {"markdown": "", "json": ""}
    return paths


def _record_evaluation_run(suite: str, metrics: dict[str, object]) -> bool:
    if not initialize_database():
        return False
    session_factory = get_session_factory()
    if session_factory is None:
        return False
    try:
        with session_factory() as session:
            session.add(
                EvaluationRunRecord(
                    suite=suite,
                    cases_total=int(metrics["cases_total"]),
                    cases_passed=int(metrics["cases_passed"]),
                    pass_rate=float(metrics["pass_rate"]),
                    latency_ms=int(metrics["latency_ms"]),
                )
            )
            session.commit()
    except Exception:
        return False
    return True
