# Enterprise Financial Intelligence Agent Platform: Ultimate Goal

## 一句話定位

`Enterprise Financial Intelligence Agent Platform` 是一個企業級 AI Agent 平台，結合 RAG、SQL Agent、金融文件分析、宏觀經濟資料、權限控制、LLMOps、監控、成本追蹤與治理文件，模擬金融公司內部的 research 與 operations automation platform

這個 project 的定位不是一般 chatbot，而是展示一個可落地、可追蹤、可監控、可治理的 enterprise AI system

## 目標職能訊號

這個 project 目標是同時展示 Senior AI Engineer 和 AI Solution Architect 能力

- 用 LLM、RAG、structured data、workflow orchestration 建立實際可用的 AI application
- 整合 SEC、FRED、PostgreSQL、Qdrant、internal policy docs 等多種資料來源
- 設計 evaluation、observability、cost tracking、risk control、governance
- 用 architecture documents、roadmap、security design、cost estimate 展示 Solution Architect 思維
- 在面試中清楚說明 business value、technical tradeoffs、production risk 和 rollout plan

## 核心模組

## Document Research Agent

使用 SEC 年報、10-K、10-Q、公司公告和 filings 做 RAG

預期能力:

- Ingest financial documents
- 對 filing text 做 parsing、chunking、embedding
- 從 vector database retrieve relevant passages
- 回答時引用 documents、chunks、accession number
- Response 顯示 used sources 和 agent trace

## Macro Analysis Agent

使用 FRED economic data 生成宏觀分析摘要

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

- 根據問題決定使用 Document Agent、Policy Agent、Macro Agent、SQL Agent、Macro + Document route，或 fallback route
- 記錄 route decision
- 回傳 multi-step trace，讓使用者知道系統用了哪些工具和資料
- 保留原有 `/api/chat` response shape，frontend 不需要大改

## Evaluation Engine

建立 evaluation datasets 和 scoring scripts，用來衡量

- Retrieval accuracy
- Answer faithfulness
- Latency
- Cost
- Hallucination rate
- Citation correctness
- Router accuracy

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

## 推薦 Tech Stack

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

## 資料來源

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

## 系統架構

```text
Frontend
  |
FastAPI Gateway
  |
Auth / RBAC / Request Logger
  |
LangGraph Orchestrator
  |
  |-- Document Research Agent -> Vector DB -> SEC filings
  |-- SQL Analytics Agent -> PostgreSQL -> financial facts
  |-- Macro Agent -> FRED API / cached macro table
  |-- Policy Agent -> Vector DB -> internal policies
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
Planned
```

Planned:

- Eval dataset expansion
- Retrieval recall
- Citation correctness
- Faithfulness score
- Hallucination checks
- Latency tracking
- Token / cost tracking
- Batch eval report

## Sprint 8: Security / Governance / Reliability

Status:

```text
Planned
```

Planned:

- PII masking
- Prompt injection detection
- RBAC
- Audit logs
- Retry / timeout
- Model fallback
- Data retention policy
- Human approval path

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

## 目前進度

```text
Sprint 1: mostly completed
Sprint 2: completed for MVP scope
Sprint 3: completed for MVP scope
Sprint 4: completed for MVP scope
Sprint 5: completed for MVP scope
Sprint 6: completed for MVP scope
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
- Frontend demo for chat、ingestion、system status、SEC controls、macro controls、SQL controls
- SEC、macro、orchestrator、SQL smoke evaluation suites

## 下一個開發步驟

```text
Start Sprint 7: LLMOps / Evaluation
```

下一步工作:

1. 擴充 evaluation dataset
2. 加入 retrieval recall 和 citation correctness scoring
3. 加入 faithfulness / hallucination checks
4. 建立 batch eval report
5. 補 latency 和 cost reporting
