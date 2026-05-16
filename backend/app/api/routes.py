from fastapi import APIRouter, HTTPException

from app.api.schemas import (
    ChatRequest,
    ChatResponse,
    CompanyFactsIngestRequest,
    CompanyFactsIngestResponse,
    ConfigStatusResponse,
    EvalRunRequest,
    IngestResponse,
    IngestRequest,
    MacroAnalyzeRequest,
    MacroAnalyzeResponse,
    MacroSeriesResponse,
    SqlAnalyzeRequest,
    SqlAnalyzeResponse,
)
from app.agents.orchestrator import build_orchestrated_chat_response
from app.services.config_service import get_config_status
from app.services.eval_service import generate_evaluation_report, run_evaluation_suite
from app.services.ingestion_service import ingest_policy_documents, ingest_sec_document
from app.services.macro_service import analyze_macro_context, get_macro_series
from app.services.sql_analytics_service import analyze_financial_facts, ingest_company_facts


router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    try:
        return build_orchestrated_chat_response(request)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.get("/config/status", response_model=ConfigStatusResponse)
def config_status() -> ConfigStatusResponse:
    return get_config_status()


@router.post("/ingest/policy", response_model=IngestResponse)
def ingest_policy(request: IngestRequest) -> IngestResponse:
    try:
        return ingest_policy_documents(request)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.post("/ingest/sec", response_model=IngestResponse)
def ingest_sec(request: IngestRequest) -> IngestResponse:
    try:
        return ingest_sec_document(request)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.post("/ingest/company-facts", response_model=CompanyFactsIngestResponse)
def ingest_facts(request: CompanyFactsIngestRequest) -> CompanyFactsIngestResponse:
    try:
        return ingest_company_facts(request)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.get("/macro/series/{series_id}", response_model=MacroSeriesResponse)
def macro_series(series_id: str) -> MacroSeriesResponse:
    try:
        return get_macro_series(series_id)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.post("/macro/analyze", response_model=MacroAnalyzeResponse)
def macro_analyze(request: MacroAnalyzeRequest) -> MacroAnalyzeResponse:
    try:
        return analyze_macro_context(request)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.post("/sql/analyze", response_model=SqlAnalyzeResponse)
def sql_analyze(request: SqlAnalyzeRequest) -> SqlAnalyzeResponse:
    try:
        return analyze_financial_facts(request)
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/evals/run")
def run_evals(request: EvalRunRequest) -> dict[str, object]:
    try:
        return run_evaluation_suite(request)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.post("/evals/report")
def eval_report(request: EvalRunRequest) -> dict[str, object]:
    try:
        return generate_evaluation_report(request)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
