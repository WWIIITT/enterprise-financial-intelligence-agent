from pydantic import BaseModel, Field


class Source(BaseModel):
    title: str
    url: str | None = None
    citation: str | None = None
    source_type: str | None = None


class TraceStep(BaseModel):
    step: str
    detail: str


class Metrics(BaseModel):
    latency_ms: int = 0
    estimated_cost_usd: float = 0
    tokens_input: int = 0
    tokens_output: int = 0


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    answer: str
    agent: str
    sources: list[Source]
    trace: list[TraceStep]
    metrics: Metrics


class ConfigStatusResponse(BaseModel):
    service: str
    llm_provider_configured: bool
    embedding_configured: bool
    database_configured: bool
    qdrant_configured: bool
    redis_configured: bool
    fred_configured: bool
    sec_user_agent_configured: bool


class IngestRequest(BaseModel):
    source: str = Field(..., min_length=1)
    source_type: str | None = None
    ticker: str | None = None
    cik: str | None = None
    limit: int = Field(default=5, ge=1, le=50)
    content: str | None = None


class IngestResponse(BaseModel):
    status: str
    source_type: str
    source: str
    documents_indexed: int = 0
    chunks_indexed: int = 0
    vector_backend: str
    message: str


class MacroSeriesResponse(BaseModel):
    series_id: str
    source: str
    observations: list[dict[str, str | float]]
    message: str


class EvalRunRequest(BaseModel):
    suite: str = "smoke"
