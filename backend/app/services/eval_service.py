from __future__ import annotations

import json
from pathlib import Path
from time import perf_counter
from typing import Any

from app.agents.orchestrator import build_orchestrated_chat_response
from app.api.schemas import ChatRequest, EvalRunRequest
from app.core.config import ROOT_DIR


SEC_CASES_PATH = ROOT_DIR / "backend" / "app" / "evals" / "sec_filing_cases.json"
MACRO_CASES_PATH = ROOT_DIR / "backend" / "app" / "evals" / "macro_cases.json"
ORCHESTRATOR_CASES_PATH = ROOT_DIR / "backend" / "app" / "evals" / "orchestrator_cases.json"


def run_evaluation_suite(request: EvalRunRequest) -> dict[str, object]:
    cases = _load_cases(request.suite)
    started = perf_counter()
    results = [_run_case(case) for case in cases]
    passed = sum(1 for result in results if result["passed"])
    latency_ms = int((perf_counter() - started) * 1000)
    total = len(results)
    return {
        "status": "completed",
        "suite": request.suite,
        "metrics": {
            "cases_total": total,
            "cases_passed": passed,
            "pass_rate": round(passed / total, 4) if total else 0.0,
            "latency_ms": latency_ms,
        },
        "results": results,
        "message": "Evaluation suite completed with deterministic routing, citation, and answer checks.",
    }


def _load_cases(suite: str) -> list[dict[str, Any]]:
    paths = [SEC_CASES_PATH]
    if MACRO_CASES_PATH.exists():
        paths.append(MACRO_CASES_PATH)
    if ORCHESTRATOR_CASES_PATH.exists():
        paths.append(ORCHESTRATOR_CASES_PATH)

    cases: list[dict[str, Any]] = []
    for path in paths:
        with path.open(encoding="utf-8") as handle:
            cases.extend(json.load(handle))
    selected = [case for case in cases if suite in {"all", case.get("suite")}]
    return selected or cases


def _run_case(case: dict[str, Any]) -> dict[str, object]:
    response = build_orchestrated_chat_response(ChatRequest(message=case["question"]))
    failures: list[str] = []

    expected_agent = case.get("expected_agent")
    if expected_agent and response.agent != expected_agent:
        failures.append(f"expected agent {expected_agent}, got {response.agent}")

    required_source_type = case.get("required_source_type")
    if required_source_type and not any(source.source_type == required_source_type for source in response.sources):
        failures.append(f"missing source type {required_source_type}")

    answer_lower = response.answer.lower()
    for term in case.get("required_answer_terms", []):
        if str(term).lower() not in answer_lower:
            failures.append(f"answer missing term {term}")

    citations = " ".join(str(source.citation or "") for source in response.sources).lower()
    for term in case.get("required_citation_terms", []):
        if str(term).lower() not in citations:
            failures.append(f"citation missing term {term}")

    return {
        "id": case["id"],
        "passed": not failures,
        "failures": failures,
        "agent": response.agent,
        "sources_count": len(response.sources),
    }
