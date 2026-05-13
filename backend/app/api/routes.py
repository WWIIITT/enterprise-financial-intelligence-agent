from fastapi import APIRouter

from app.api.schemas import (
    ChatRequest,
    ChatResponse,
    ConfigStatusResponse,
    EvalRunRequest,
    IngestResponse,
    IngestRequest,
    MacroSeriesResponse,
)
from app.services.config_service import get_config_status
from app.services.ingestion_service import ingest_policy_documents, ingest_sec_document
from app.services.rag_service import build_rag_chat_response


router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    return build_rag_chat_response(request)


@router.get("/config/status", response_model=ConfigStatusResponse)
def config_status() -> ConfigStatusResponse:
    return get_config_status()


@router.post("/ingest/policy", response_model=IngestResponse)
def ingest_policy(request: IngestRequest) -> IngestResponse:
    return ingest_policy_documents(request)


@router.post("/ingest/sec", response_model=IngestResponse)
def ingest_sec(request: IngestRequest) -> IngestResponse:
    return ingest_sec_document(request)


@router.get("/macro/series/{series_id}", response_model=MacroSeriesResponse)
def macro_series(series_id: str) -> MacroSeriesResponse:
    return MacroSeriesResponse(
        series_id=series_id,
        source="FRED",
        observations=[],
        message="Macro data connector placeholder. Add FRED_API_KEY to enable live ingestion.",
    )


@router.post("/evals/run")
def run_evals(request: EvalRunRequest) -> dict[str, object]:
    return {
        "status": "completed",
        "suite": request.suite,
        "metrics": {
            "retrieval_recall": None,
            "faithfulness": None,
            "latency_ms_p50": None,
            "estimated_cost_usd": None,
        },
        "message": "Evaluation runner placeholder. Add test cases in backend/app/evals.",
    }
