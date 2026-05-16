from __future__ import annotations

from time import perf_counter
from typing import Literal, TypedDict

from langgraph.graph import END, StateGraph

from app.api.schemas import ChatRequest, ChatResponse, Metrics, Source, TraceStep
from app.services.macro_service import compose_macro_answer, get_macro_series, infer_macro_series, is_macro_question
from app.services.metadata_service import record_request_log
from app.services.rag_service import build_retrieval_chat_response


RouteName = Literal["policy", "document", "macro", "macro_document", "unknown"]


class OrchestratorState(TypedDict, total=False):
    request: ChatRequest
    route: RouteName
    response: ChatResponse
    trace: list[TraceStep]
    started_at: float


def build_orchestrated_chat_response(request: ChatRequest) -> ChatResponse:
    graph = _build_graph()
    state: OrchestratorState = {
        "request": request,
        "trace": [TraceStep(step="receive", detail=f"Received {len(request.message)} characters.")],
        "started_at": perf_counter(),
    }
    final_state = graph.invoke(state)
    response = final_state["response"]
    record_request_log(request.message, response.agent, len(response.sources), response.metrics.latency_ms)
    return response


def route_question(message: str) -> RouteName:
    lowered = message.lower()
    if _has_macro_document_intent(lowered):
        return "macro_document"
    if is_macro_question(message):
        return "macro"
    if _has_policy_intent(lowered):
        return "policy"
    if _has_document_intent(lowered):
        return "document"
    return "unknown"


def _build_graph():
    graph = StateGraph(OrchestratorState)
    graph.add_node("router", _router_node)
    graph.add_node("policy", _policy_compliance_node)
    graph.add_node("document", _document_research_node)
    graph.add_node("macro", _macro_analysis_node)
    graph.add_node("macro_document", _multi_agent_node)
    graph.add_node("fallback", _fallback_node)
    graph.set_entry_point("router")
    graph.add_conditional_edges(
        "router",
        _route_edge,
        {
            "policy": "policy",
            "document": "document",
            "macro": "macro",
            "macro_document": "macro_document",
            "unknown": "fallback",
        },
    )
    for node_name in ("policy", "document", "macro", "macro_document", "fallback"):
        graph.add_edge(node_name, END)
    return graph.compile()


def _router_node(state: OrchestratorState) -> OrchestratorState:
    request = state["request"]
    route = route_question(request.message)
    trace = [*state.get("trace", []), TraceStep(step="route", detail=f"Selected {route} route.")]
    return {**state, "route": route, "trace": trace}


def _route_edge(state: OrchestratorState) -> RouteName:
    return state.get("route", "unknown")


def _policy_compliance_node(state: OrchestratorState) -> OrchestratorState:
    response = build_retrieval_chat_response(state["request"], start=state["started_at"], log_request=False)
    return _with_response(
        state,
        response,
        selected_agent="policy-compliance-agent" if response.agent != "rag-orchestrator-empty-index" else response.agent,
        step="policy_compliance",
        detail="Queried policy RAG evidence and synthesized a cited compliance response.",
    )


def _document_research_node(state: OrchestratorState) -> OrchestratorState:
    response = build_retrieval_chat_response(state["request"], start=state["started_at"], log_request=False)
    return _with_response(
        state,
        response,
        selected_agent="document-research-agent" if response.agent != "rag-orchestrator-empty-index" else response.agent,
        step="document_research",
        detail="Queried document RAG evidence and synthesized a cited filing response.",
    )


def _macro_analysis_node(state: OrchestratorState) -> OrchestratorState:
    request = state["request"]
    series = [get_macro_series(series_id, limit=8) for series_id in infer_macro_series(request.message)]
    sources = [
        Source(
            title=item.title or item.series_id,
            url=f"https://fred.stlouisfed.org/series/{item.series_id}",
            citation=f"FRED {item.series_id}",
            source_type="macro",
        )
        for item in series
    ]
    response = ChatResponse(
        answer=compose_macro_answer(request.message, series),
        agent="macro-analysis-agent",
        sources=sources,
        trace=[],
        metrics=_metrics(state),
    )
    return _with_response(
        state,
        response,
        selected_agent="macro-analysis-agent",
        step="macro_analysis",
        detail=f"Loaded {len(series)} macro series from FRED/cache/sample data.",
    )


def _multi_agent_node(state: OrchestratorState) -> OrchestratorState:
    request = state["request"]
    series = [get_macro_series(series_id, limit=8) for series_id in infer_macro_series(request.message)]
    retrieval_response = build_retrieval_chat_response(request, start=state["started_at"], log_request=False)
    sec_sources = [source for source in retrieval_response.sources if source.source_type == "sec"]
    sec_citations = [source.citation for source in sec_sources if source.citation]
    macro_sources = [
        Source(
            title=item.title or item.series_id,
            url=f"https://fred.stlouisfed.org/series/{item.series_id}",
            citation=f"FRED {item.series_id}",
            source_type="macro",
        )
        for item in series
    ]
    response = ChatResponse(
        answer=compose_macro_answer(request.message, series, sec_citations=sec_citations),
        agent="macro-document-orchestrator",
        sources=[*macro_sources, *sec_sources[:3]],
        trace=[],
        metrics=_metrics(state),
    )
    return _with_response(
        state,
        response,
        selected_agent="macro-document-orchestrator",
        step="synthesize",
        detail=f"Combined {len(series)} macro series with {len(sec_sources[:3])} SEC source(s).",
    )


def _fallback_node(state: OrchestratorState) -> OrchestratorState:
    response = build_retrieval_chat_response(state["request"], start=state["started_at"], log_request=False)
    return _with_response(
        state,
        response,
        selected_agent=response.agent,
        step="fallback",
        detail="No specialized route matched; used retrieval fallback and no-answer safeguards.",
    )


def _with_response(
    state: OrchestratorState,
    response: ChatResponse,
    selected_agent: str,
    step: str,
    detail: str,
) -> OrchestratorState:
    trace = [
        *state.get("trace", []),
        TraceStep(step=step, detail=detail),
        TraceStep(step="respond", detail=f"Returned response from {selected_agent}."),
    ]
    finalized = response.model_copy(
        update={
            "agent": selected_agent,
            "trace": trace,
            "metrics": _metrics(state),
        }
    )
    return {**state, "response": finalized, "trace": trace}


def _metrics(state: OrchestratorState) -> Metrics:
    return Metrics(latency_ms=int((perf_counter() - state["started_at"]) * 1000))


def _has_policy_intent(lowered: str) -> bool:
    return any(
        term in lowered
        for term in (
            "policy",
            "approved use",
            "prohibited",
            "privacy",
            "pii",
            "compliance",
            "governance",
            "review requirement",
            "model risk",
        )
    )


def _has_document_intent(lowered: str) -> bool:
    return any(
        term in lowered
        for term in (
            "apple",
            "aapl",
            "company",
            "filing",
            "10-k",
            "10-q",
            "sec",
            "revenue",
            "risk",
            "risks",
            "supply chain",
        )
    )


def _has_macro_document_intent(lowered: str) -> bool:
    has_company_context = any(term in lowered for term in ("apple", "aapl", "company", "valuation", "revenue"))
    return has_company_context and is_macro_question(lowered)
