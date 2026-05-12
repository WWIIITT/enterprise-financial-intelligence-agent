from fastapi import APIRouter

from app.api.schemas import (
    ChatRequest,
    ChatResponse,
    ConfigStatusResponse,
    EvalRunRequest,
    IngestRequest,
    MacroSeriesResponse,
)
from app.services.chat_service import build_placeholder_chat_response
from app.services.config_service import get_config_status


router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    return build_placeholder_chat_response(request)


@router.get("/config/status", response_model=ConfigStatusResponse)
def config_status() -> ConfigStatusResponse:
    return get_config_status()


@router.post("/ingest/policy")
def ingest_policy(request: IngestRequest) -> dict[str, str]:
    return {
        "status": "accepted",
        "source_type": "policy",
        "source": request.source,
        "message": "Policy ingestion placeholder registered.",
    }


@router.post("/ingest/sec")
def ingest_sec(request: IngestRequest) -> dict[str, str]:
    return {
        "status": "accepted",
        "source_type": "sec",
        "source": request.source,
        "message": "SEC ingestion placeholder registered.",
    }


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
