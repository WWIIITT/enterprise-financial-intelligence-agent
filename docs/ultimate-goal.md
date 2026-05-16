# Enterprise Financial Intelligence Agent Platform: Ultimate Goal

## 一句話定位

`Enterprise Financial Intelligence Agent Platform` 是一個企業級 AI Agent 平台，結合 RAG、SQL Agent、金融文件分析、宏觀經濟資料、權限與治理、LLMOps、監控、成本追蹤和架構文件，模擬金融公司內部 research 與 operations automation platform

這個 project 的定位不是一般 chatbot，而是展示一個可落地、可追蹤、可監控、可治理的 enterprise AI system

## 目標職能訊號

這個 project 目標是同時展示 Senior AI Engineer 和 AI Solution Architect 能力

- 用 LLM、RAG、structured data、workflow orchestration 建立可用的 AI application
- 整合 SEC、FRED、PostgreSQL、Qdrant、internal policy docs 等多種資料來源
- 設計 evaluation、observability、cost tracking、risk control、governance
- 用 architecture documents、roadmap、security design、cost estimate 展示 Solution Architect 思維
- 在面試中清楚說明 business value、technical tradeoffs、production risk 和 rollout plan

## Core Modules

## Document Research Agent

使用 SEC 年報、10-K、10-Q、公司公告和 filings 做 RAG

預期能力:

- Ingest financial documents
- 對 filing text 做 parsing、chunking、embedding
- 從 vector database retrieve relevant passages
- 回答時引用 documents、chunks、accession number
- Response 顯示 used sources 和 agent trace

## Macro Analysis Agent

使用 FRED economic data 產生宏觀分析摘要

支援資料:

- Interest rates
- CPI
- Unemployment rate
- GDP
- 10-year Treasury yield

## SQL Analytics Agent

對 PostgreSQL 裡的 structured financial facts 做 deterministic analytics

目前能力:

- Ingest SEC Company Facts 或 sample financial facts
- 儲存 revenue、net income、assets、liabilities、cash、operating cash flow、shares
- 使用 safe query templates
- 不接受 raw SQL
- 不使用 LLM-generated SQL
- 回傳 financial trend summary、facts、sources、trace

## Policy & Compliance Agent

讀取自製 enterprise policy documents，回答是否合規

Policy documents:

- AI Usage Policy
- Investment Research Review Policy
- Data Privacy and PII Handling Policy
- Model Risk Management Policy
- Client Communication Policy

## Workflow Orchestrator

使用 LangGraph 做 deterministic routing

目前能力:

- 根據問題決定使用 Document Agent、Policy Agent、Macro Agent、SQL Agent、Macro + Document route 或 fallback route
- 記錄 route decision
- 回傳 multi-step trace，讓使用者知道系統用了哪些工具和資料
- 保留原有 `/api/chat` response shape，frontend 不需要大改

## Evaluation Engine

建立 evaluation datasets、scoring scripts 和 report generator，用來衡量:

- Retrieval accuracy
- Answer faithfulness
- Latency
- Cost
- Hallucination rate
- Citation correctness
- Router accuracy
- Source coverage
- Evaluation report quality

## Security / Governance Guardrails

在 agent routing 前執行 deterministic security preflight

目前能力:

- PII masking
- Prompt injection detection
- Policy risk classification
- Block unsafe requests before retrieval or tool use
- Mask sensitive values before agent routing
- Security audit logs with message hash only
- `security-smoke` evaluation suite

## Observability Dashboard

監控 runtime behavior 和 production signals

- Token usage
- Latency
- Error rate
- Agent route
- Retrieval score
- Cost per request

## Architecture Pack

Solution Architect deliverables:

- Architecture diagram
- Data flow diagram
- Security design
- Risk controls
- Cost estimate
- Roadmap
- Governance documents
- Demo script
- Interview talking points

## Recommended Tech Stack

Backend:

- Python
- FastAPI
- Pydantic
- SQLAlchemy

Agent / LLM:

- LangGraph
- LangChain
- OpenAI API or Azure OpenAI
- OpenAI-compatible provider
- Function calling
- Structured output

RAG:

- Qdrant or Weaviate
- OpenAI embeddings or sentence-transformers
- Hybrid search
- Reranking
- Citation-aware answer generation

Database:

- PostgreSQL
- Redis

Data Pipeline:

- Python ETL
- pandas
- SEC EDGAR API
- SEC Company Facts API
- FRED API

LLMOps / Monitoring:

- LangSmith or MLflow
- Prometheus
- Grafana
- OpenTelemetry
- Custom evaluation scripts

Frontend:

- React
- TypeScript
- Vite

## Data Sources

SEC EDGAR APIs:
https://www.sec.gov/search-filings/edgar-application-programming-interfaces

FRED API:
https://fred.stlouisfed.org/docs/api/fred/

SEC Company Facts API:

- Revenue
- Net income
- Assets
- Liabilities
- Equity
- Shares
- Company comparison

Internal policy documents:

- AI Usage Policy
- Investment Research Review Policy
- Data Privacy and PII Handling Policy
- Model Risk Management Policy
- Client Communication Policy

## System Architecture

```text
Frontend
  |
FastAPI Gateway
  |
Security Preflight / Request Logger
  |
LangGraph Orchestrator
  |
  |-- Document Research Agent -> Vector DB -> SEC filings
  |-- SQL Analytics Agent -> PostgreSQL -> financial facts
  |-- Macro Agent -> FRED API / cached macro table
  |-- Policy Agent -> Vector DB -> internal policies
  |-- Security Governance Agent -> guardrail checks / audit logs
  |-- Evaluator Agent -> eval dataset / scoring
  |
Observability Layer
  |-- LangSmith / MLflow
  |-- Prometheus
  |-- Grafana
  |-- Cost logs
```

## Complete Sprint Roadmap

## Sprint 1: Project Skeleton + RAG MVP Foundation

Status:

```text
Mostly completed
```

Completed:

- FastAPI backend skeleton
- React + TypeScript frontend
- Docker Compose for PostgreSQL、Qdrant、Redis
- `.env` config
- Policy document ingestion
- SEC sample ingestion
- Basic chunking
- Qdrant indexing fallback
- In-memory dev RAG fallback
- `/api/chat`
- Citation-shaped answer
- Browser demo UI
- System status panel

## Sprint 2: Production-Grade RAG

Status:

```text
Completed for MVP scope
```

Completed:

- Real embedding client
- Provider embedding API key / base URL config
- Qdrant real-vector upsert and search path
- Policy ingestion with provider embeddings
- SEC sample ingestion with provider embeddings
- Lightweight reranking
- Source-intent filtering
- Low-confidence no-answer behavior

## Sprint 3: SEC EDGAR Live Ingestion

Status:

```text
Completed for MVP scope
```

Completed:

- SEC EDGAR connector
- Ticker / CIK lookup
- Company submissions lookup
- Latest 10-K / 10-Q ingestion
- Filing selection by year and accession number
- Raw filing storage under `data/raw/sec/`
- SEC section parser
- Request retry / throttling
- Live SEC ingestion UI controls
- SEC risk answer synthesis
- SEC evaluation smoke cases

## Sprint 4: Macro Analysis Agent

Status:

```text
Completed for MVP scope
```

Completed:

- FRED client with live API path
- Deterministic sample fallback when `FRED_API_KEY` is missing
- Supported series: `FEDFUNDS`、`CPIAUCSL`、`UNRATE`、`GDP`、`DGS10`
- PostgreSQL macro observation cache
- `/api/macro/series/{series_id}`
- `/api/macro/analyze`
- Macro-aware chat routing
- Company + macro question support
- Frontend Macro Analysis controls
- `macro-smoke` evaluation suite

## Sprint 5: LangGraph Workflow Orchestrator

Status:

```text
Completed for MVP scope
```

Completed:

- LangGraph `StateGraph` orchestrator
- Deterministic router
- Document Research route
- Policy Compliance route
- Macro Analysis route
- Macro + Document route
- Fallback route
- Unified route trace
- `/api/chat` keeps the same response shape
- `orchestrator-smoke` evaluation suite

## Sprint 6: SQL Analytics Agent

Status:

```text
Completed for MVP scope
```

Completed:

- PostgreSQL financial facts schema
- SEC Company Facts client
- Deterministic AAPL sample fallback
- `/api/ingest/company-facts`
- `/api/sql/analyze`
- Safe query templates with predefined metrics only
- LangGraph SQL route
- Frontend SQL Analytics controls
- `sql-smoke` evaluation suite

## Sprint 7: LLMOps / Evaluation

Status:

```text
Completed for MVP scope
```

Completed:

- Expanded eval case schema
- Route accuracy scoring
- Source coverage scoring
- Citation correctness scoring
- Answer term / faithfulness proxy scoring
- Hallucination-risk flags
- Average and p95 latency summary
- `/api/evals/report`
- Markdown and JSON report output under `data/reports/`
- Evaluation run DB records
- Frontend eval controls

## Sprint 8: Security / Governance / Reliability

Status:

```text
Completed for MVP scope
```

Completed:

- Sprint 7 SEC eval expectation cleanup
- Deterministic security guardrail service
- PII masking for email、phone、SSN、payment card-like values、secret-like tokens
- Prompt injection detection
- `/api/security/check`
- `/api/chat` security preflight before LangGraph routing
- Blocked request response through `security-governance-agent`
- Masked request routing with redacted input
- Security audit records with message hash only
- Frontend System Status / Governance controls
- `security-smoke` evaluation suite

## Sprint 9: Observability Dashboard

Status:

```text
Planned
```

Planned:

- Token usage
- Latency
- Error rate
- Agent route
- Retrieval score
- Cost per request
- Prometheus / Grafana or custom UI

## Sprint 10: Architecture Pack / Portfolio Polish

Status:

```text
Planned
```

Planned:

- Architecture diagram
- Data flow diagram
- Security design
- Cost estimate
- Risk register
- Deployment roadmap
- Evaluation report
- Demo script
- Interview talking points

## Current Progress

```text
Sprint 1: mostly completed
Sprint 2: completed for MVP scope
Sprint 3: completed for MVP scope
Sprint 4: completed for MVP scope
Sprint 5: completed for MVP scope
Sprint 6: completed for MVP scope
Sprint 7: completed for MVP scope
Sprint 8: completed for MVP scope
```

目前系統能力:

- Policy RAG
- SEC sample and live SEC filing ingestion
- Provider embeddings + Qdrant retrieval
- Citation-aware answers
- SEC risk synthesis
- FRED macro series API
- Macro analysis endpoint
- LangGraph Workflow Orchestrator
- SQL Analytics Agent
- SEC Company Facts sample/live ingestion
- Deterministic Evaluation Engine
- Markdown / JSON evaluation reports
- Security / Governance Guardrails
- Frontend demo for chat、ingestion、system status、SEC controls、macro controls、SQL controls、governance controls
- SEC、macro、orchestrator、SQL、security smoke evaluation suites

## Next Development Step

```text
Start Sprint 9: Observability Dashboard
```

下一步工作:

1. 建立 request metrics API
2. 顯示 route distribution
3. 顯示 latency p50 / p95
4. 顯示 error rate
5. 顯示 estimated cost per request
