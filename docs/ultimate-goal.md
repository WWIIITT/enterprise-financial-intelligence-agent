# Enterprise Financial Intelligence Agent Platform：Ultimate Goal

## One-Line Positioning

`Enterprise Financial Intelligence Agent Platform` 是一個企業級 AI Agent 平台，結合 RAG、SQL Agent、金融資料分析、宏觀經濟資料、權限控制、LLMOps、監控、成本追蹤與治理文件。

這個專案模擬金融公司內部的 research 與 operations automation platform。目標不是普通 chatbot，而是展示可落地、可監控、可治理的 enterprise AI system。

## Target Role Signal

這個 project 目標是同時展示 Senior AI Engineer 與 AI Solution Architect 能力：

- 使用 LLM、RAG、structured data、workflow orchestration 建立實際 AI application。
- 整合 SEC、FRED、PostgreSQL、Qdrant、internal policy docs 等資料來源。
- 設計 evaluation、observability、cost tracking、risk control、governance。
- 用 architecture documents、roadmap、security design、cost estimate 展示 Solution Architect 思維。
- 能在面試中清楚說明 business value、technical tradeoffs、production risk 與 rollout plan。

## Core Modules

## Document Research Agent

使用 SEC 年報、10-K、10-Q、公司公告與 filings 做 RAG。

預期能力：

- Ingest financial documents。
- 對 filing text 做 parsing、chunking、embedding。
- 從 vector database retrieve relevant passages。
- 回答問題時引用來源。
- Response 顯示使用了哪些 documents / chunks。

## Macro Analysis Agent

使用 FRED economic data 生成宏觀分析摘要。

資料例子：

- Interest rates。
- CPI。
- Unemployment rate。
- GDP。
- Yield curve indicators。

## SQL Analytics Agent

對 PostgreSQL 裡的 structured financial data 做查詢。

資料例子：

- 公司財務指標。
- 行業分類。
- Revenue / margin changes。
- Balance sheet metrics。
- SEC Company Facts API 轉換後的 financial facts tables。

## Policy & Compliance Agent

讀取自製企業政策文件，回答「是否合規」。

政策文件：

- AI Usage Policy。
- Investment Research Review Policy。
- Data Privacy and PII Handling Policy。
- Model Risk Management Policy。
- Client Communication Policy。

## Workflow Orchestrator

使用 LangGraph 做 routing。

預期能力：

- 根據問題決定使用 Document Agent、SQL Agent、Macro Agent、Policy Agent，或多個 agents 合作。
- 記錄 route decision。
- 回傳 trace，讓使用者知道系統用了哪些工具和資料。

## Evaluation Engine

建立測試集和 scoring scripts，用來衡量：

- Retrieval accuracy。
- Answer faithfulness。
- Latency。
- Cost。
- Hallucination rate。
- Citation correctness。
- Router accuracy。

## Observability Dashboard

監控 runtime behavior 和 production signals：

- Token usage。
- Latency。
- Error rate。
- Agent route。
- Retrieval score。
- Cost per request。

## Architecture Pack

Solution Architect deliverables：

- Architecture diagram。
- Data flow diagram。
- Security design。
- Risk controls。
- Cost estimate。
- Roadmap。
- Governance document。
- Demo script。
- Interview talking points。

## Recommended Tech Stack

Backend：

- Python。
- FastAPI。
- Pydantic。
- SQLAlchemy。

Agent / LLM：

- LangGraph。
- LangChain。
- OpenAI API or Azure OpenAI。
- OpenAI-compatible provider。
- Function calling。
- Structured output。

RAG：

- Qdrant 或 Weaviate。
- OpenAI embeddings 或 sentence-transformers。
- Hybrid search。
- Reranking。
- Citation-aware answer generation。

Database：

- PostgreSQL。
- Redis。

Data Pipeline：

- Python ETL。
- pandas。
- SEC EDGAR API。
- FRED API。

LLMOps / Monitoring：

- LangSmith 或 MLflow。
- Prometheus。
- Grafana。
- OpenTelemetry。
- Custom evaluation scripts。

Frontend：

- React + TypeScript。
- Vite。

## Data Sources

SEC EDGAR APIs：

https://www.sec.gov/search-filings/edgar-application-programming-interfaces

FRED API：

https://fred.stlouisfed.org/docs/api/fred/

SEC Company Facts API：

- Revenue。
- Net income。
- Assets。
- Liabilities。
- Equity。
- Shares。
- Company comparison。

Internal policy documents：

- AI Usage Policy。
- Investment Research Review Policy。
- Data Privacy and PII Handling Policy。
- Model Risk Management Policy。
- Client Communication Policy。

## System Architecture

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

## Sprint 1：Project Skeleton + RAG MVP Foundation

目標：

```text
FastAPI + Docker services + basic RAG + citation answer + frontend demo
```

內容：

- 建立 repo structure：`backend/`, `frontend/`, `data/`, `docs/`, `infra/`。
- FastAPI skeleton。
- React + TypeScript frontend。
- Docker Compose：PostgreSQL、Qdrant、Redis。
- `.env` config。
- Policy document ingestion。
- SEC sample ingestion。
- Basic chunking。
- Qdrant indexing fallback。
- In-memory dev RAG fallback。
- `/api/chat`。
- Citation-shaped answer。
- Browser demo UI。
- System status panel。
- Request trace / metrics placeholder。

目前狀態：

```text
大部分已完成。Demo-grade RAG 已可用。
```

## Sprint 2：Production-Grade RAG

目標：

```text
real embeddings + persistent Qdrant + cleaner retrieval + better citations
```

內容：

- 加入 real embedding client。
- 用正式 embedding vector 取代 hash embedding。
- Qdrant 成為主要 retrieval backend。
- PostgreSQL 儲存 document metadata、chunk metadata、request logs。
- 改善 chunking strategy。
- 改善 citation format。
- 加入 reranking。
- 加入 no-answer behavior。
- 加入 better answer synthesis。

目前狀態：

```text
Core completed for MVP scope。
Provider embedding、persistent Qdrant retrieval、policy ingestion、SEC sample ingestion、source-intent reranking、low-confidence no-answer 已完成並通過 end-to-end validation。
Retrieval quality hardening 會在後續 sprint 持續改善。
```

## Sprint 3：SEC EDGAR Live Ingestion

目標：

```text
real SEC filing ingestion
```

內容：

- 用 SEC EDGAR API 抓 filings。
- 支援 ticker / CIK lookup。
- 抓 10-K / 10-Q。
- 儲存 raw filing 到 `data/raw/`。
- Parser 清理 filing text。
- Chunk + embed + index。
- 回答時引用 SEC source。

目前狀態：

```text
尚未開始。目前只有 SEC sample ingestion。
```

## Sprint 4：Macro Analysis Agent

目標：

```text
FRED macro data analysis
```

內容：

- FRED API connector。
- 拉取 CPI、GDP、unemployment、interest rates。
- Cache macro series。
- 生成 macro summary。
- 支援 macro + company risk 問題。

目前狀態：

```text
尚未開始。
```

## Sprint 5：LangGraph Workflow Orchestrator

目標：

```text
agent routing
```

內容：

- LangGraph router。
- Document Research Agent。
- Policy Compliance Agent。
- Macro Analysis Agent。
- 後續加入 SQL Analytics Agent。
- Response 顯示 selected route。
- Multi-agent trace。

目前狀態：

```text
尚未開始。目前只有 simple RAG orchestrator。
```

## Sprint 6：SQL Analytics Agent

目標：

```text
structured financial data analytics
```

內容：

- PostgreSQL financial facts schema。
- SEC Company Facts ingestion。
- SQL query tool。
- Safe SQL generation。
- Financial metrics analysis。
- Company / sector comparison。

目前狀態：

```text
尚未開始。
```

## Sprint 7：LLMOps / Evaluation

目標：

```text
evaluation + quality measurement
```

內容：

- Eval dataset。
- Retrieval recall。
- Citation correctness。
- Faithfulness score。
- Hallucination checks。
- Latency tracking。
- Token / cost tracking。
- Batch eval report。

目前狀態：

```text
只有 evaluation plan 文件，engine 尚未實作。
```

## Sprint 8：Security / Governance / Reliability

目標：

```text
enterprise controls
```

內容：

- PII masking。
- Prompt injection detection。
- RBAC。
- Audit logs。
- Retry / timeout。
- Model fallback。
- Data retention policy。
- Human approval path。

目前狀態：

```text
Enterprise policy docs 已建立，runtime controls 尚未實作。
```

## Sprint 9：Observability Dashboard

目標：

```text
monitoring dashboard
```

內容：

- Token usage。
- Latency。
- Error rate。
- Agent route。
- Retrieval score。
- Cost per request。
- Prometheus / Grafana or custom UI。

目前狀態：

```text
Frontend 只有 basic metrics placeholder。
```

## Sprint 10：Architecture Pack / Portfolio Polish

目標：

```text
Solution Architect deliverables
```

內容：

- Architecture diagram。
- Data flow diagram。
- Security design。
- Cost estimate。
- Risk register。
- Deployment roadmap。
- Evaluation report。
- Demo script。
- Interview talking points。

目前狀態：

```text
已有初版 docs，還未完成 full architecture pack。
```

## Current Progress

目前完成度：

```text
Sprint 1：80-90% completed
Sprint 2：core completed for MVP scope
Sprint 3：ready to start
```

已完成：

- FastAPI backend skeleton。
- React + TypeScript frontend。
- Docker Compose services。
- PostgreSQL / Qdrant / Redis local setup。
- `.env` config loading。
- `/health`。
- `/api/config/status`。
- `/api/ingest/policy`。
- `/api/ingest/sec`。
- `/api/chat`。
- Policy docs ingestion。
- SEC sample ingestion。
- Basic local RAG。
- Qdrant indexing when available。
- In-memory fallback。
- Citation-shaped response。
- Markdown-like answer rendering。
- Agent trace。
- Metrics placeholder。
- Browser UI chat console。
- Browser ingestion buttons。
- System status panel。
- Improved responsive layout。
- Enterprise-style policy documents。
- README running process。
- Ultimate goal / roadmap / architecture docs。
- Backend tests passing。
- Frontend build passing。
- Provider embedding client。
- Separate embedding provider API key / base URL config。
- Qdrant real-vector upsert / search path。
- Qdrant ingestion end-to-end validation。
- Policy ingestion with provider embeddings。
- SEC sample ingestion with provider embeddings。
- Lightweight reranking。
- Source-intent filtering for company risk questions。
- Low-confidence no-answer behavior。

目前所在階段：

```text
Phase 3：SEC EDGAR Live Ingestion
Stage：Sprint 3 started
Current：已加入 SEC EDGAR connector 初版，下一步是 harden section parsing、filing selection、UI controls
```

更精準地說：

```text
已完成 demo-grade RAG
已完成 Sprint 2 production-grade retrieval core
已開始 Sprint 3 SEC EDGAR live ingestion
```

## Next Development Step

下一個最值得做的 task：

```text
Implement SEC EDGAR live filing ingestion
```

具體工作：

1. 建立 SEC EDGAR connector。
2. 加入 ticker -> CIK lookup。
3. 讀取 company submissions metadata。
4. 支援 10-K / 10-Q filing selection。
5. 下載 filing text 或 HTML 到 `data/raw/`。
6. Parse filing sections，先聚焦 business、risk factors、MD&A。
7. Chunk + embed + index into Qdrant。
8. Citation 顯示 accession number、form type、filing date、section。
9. 更新 `/api/ingest/sec`，讓它支援 live EDGAR source，同時保留 sample fallback。

這一步做完，project 會從「sample RAG」升級成「real financial document RAG」。
