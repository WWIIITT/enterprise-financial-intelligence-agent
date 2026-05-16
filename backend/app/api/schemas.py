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


class SecurityCheckRequest(BaseModel):
    message: str = Field(..., min_length=1)
    role: str = Field(default="research_analyst", min_length=1)


class SecurityFinding(BaseModel):
    category: str
    finding_type: str
    severity: str
    description: str
    replacement: str | None = None


class SecurityCheckResponse(BaseModel):
    status: str
    risk_level: str
    action: str
    masked_message: str
    findings: list[SecurityFinding]
    policy_tags: list[str]
    recommended_handling: str
    trace: list[TraceStep]


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
    form_type: str | None = None
    filing_year: int | None = Field(default=None, ge=1994, le=2100)
    accession_number: str | None = None
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
    title: str = ""
    units: str = ""
    source: str
    observations: list[dict[str, str | float]]
    summary: str = ""
    cache_status: str = "unknown"
    message: str


class MacroAnalyzeRequest(BaseModel):
    series_ids: list[str] = Field(default_factory=lambda: ["FEDFUNDS", "CPIAUCSL", "UNRATE"])
    question: str = Field(..., min_length=1)
    limit: int = Field(default=8, ge=1, le=60)


class MacroAnalyzeResponse(BaseModel):
    answer: str
    agent: str
    series: list[MacroSeriesResponse]
    sources: list[Source]
    trace: list[TraceStep]
    metrics: Metrics


class CompanyFactsIngestRequest(BaseModel):
    ticker: str = Field(default="AAPL", min_length=1)
    cik: str | None = None
    source: str = "sec-company-facts"
    use_sample_fallback: bool = True


class CompanyFactsIngestResponse(BaseModel):
    status: str
    ticker: str
    cik: str
    company_name: str
    facts_indexed: int
    source: str
    message: str


class FinancialFact(BaseModel):
    ticker: str
    cik: str
    company_name: str
    concept: str
    label: str
    unit: str
    fiscal_year: int
    fiscal_period: str
    form_type: str
    filed_date: str
    value: float
    source: str
    accession_number: str = ""


class SqlAnalyzeRequest(BaseModel):
    ticker: str = Field(default="AAPL", min_length=1)
    metric: str = Field(default="revenue", min_length=1)
    period: str = Field(default="annual", pattern="^(annual|quarterly)$")
    limit: int = Field(default=5, ge=1, le=20)


class SqlAnalyzeResponse(BaseModel):
    answer: str
    agent: str
    facts: list[FinancialFact]
    sources: list[Source]
    trace: list[TraceStep]
    metrics: Metrics


class EvalRunRequest(BaseModel):
    suite: str = "smoke"
