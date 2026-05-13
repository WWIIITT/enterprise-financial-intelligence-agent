# Enterprise Financial Intelligence Agent Platform：Ultimate Goal

## One-Line Positioning

`Enterprise Financial Intelligence Agent Platform` 是一個企業級 AI Agent 平台，結合 RAG、SQL Agent、金融資料分析、宏觀經濟資料、權限控制、LLMOps、監控、成本追蹤與治理文件。

這個專案模擬金融公司內部的 research 與 operations automation platform，目標不是做一個普通 chatbot，而是展示可落地、可監控、可治理的 enterprise AI system。

## Target Role Signal

Senior AI Engineer 和 AI Solution Architect 的能力高度重疊。這個 project 要展示的不只是模型調用，而是完整系統設計與工程落地能力：

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
- 回答問題時必須引用來源。
- Response 要顯示使用了哪些 documents / chunks。

## Macro Analysis Agent

使用 FRED economic data 生成宏觀分析摘要。

資料例子：

- Interest rates。
- CPI。
- Unemployment rate。
- GDP。
- Yield curve indicators。

預期能力：

- 從 FRED API 拉取或 cache macro series。
- 分析近期趨勢。
- 將 macro changes 連結到公司 revenue、valuation、risk outlook。

## SQL Analytics Agent

對 PostgreSQL 裡的 structured financial data 做查詢。

資料例子：

- 公司財務指標。
- 行業分類。
- Revenue / margin changes。
- Balance sheet metrics。
- SEC Company Facts API 轉換後的 financial facts tables。

預期能力：

- 將 user intent 轉成受控 SQL query。
- 只查詢 approved tables。
- 用 business language 解釋查詢結果。
- 避免 unrestricted SQL 或 unsafe query。

## Policy & Compliance Agent

讀取自製企業政策文件，回答「是否合規」。

政策文件例子：

- AI Usage Policy。
- Investment Research Review Policy。
- Data Privacy and PII Handling Policy。
- Model Risk Management Policy。
- Client Communication Policy。

預期能力：

- 判斷某個 workflow 或 user request 是否符合 policy。
- 引用相關 policy section。
- 在證據不足時明確表示 uncertainty。
- 提供 escalation path。

## Workflow Orchestrator

使用 LangGraph 做 routing。

預期能力：

- 根據問題決定使用 Document Agent、SQL Agent、Macro Agent、Policy Agent，或多個 agents 合作。
- 記錄 route decision。
- 回傳 trace，讓使用者知道系統用了哪些工具和資料。
- 支援 multi-agent 問題，例如：

```text
Analyze how rising interest rates may affect Apple's revenue and valuation risk.
```

## Evaluation Engine

建立測試集和 scoring scripts，用來衡量系統品質。

評估指標：

- Retrieval accuracy。
- Answer faithfulness。
- Latency。
- Cost。
- Hallucination rate。
- Citation correctness。
- Router accuracy。

預期能力：

- 執行 smoke tests。
- 執行 RAG factual tests。
- 執行 policy compliance tests。
- 執行 macro analysis tests。
- 產出可以放入 portfolio 的 evaluation report。

## Observability Dashboard

監控 runtime behavior 和 production signals。

追蹤指標：

- Token usage。
- Latency。
- Error rate。
- Agent route。
- Retrieval score。
- Cost per request。

可用工具：

- LangSmith。
- MLflow。
- Prometheus。
- Grafana。
- Custom request logs。

## Architecture Pack

這是 Level 5 / Solution Architect 定位的重點。

最終交付：

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

## Backend

- Python。
- FastAPI。
- Pydantic。
- SQLAlchemy。

## Agent / LLM

- LangGraph。
- LangChain。
- OpenAI API or Azure OpenAI。
- OpenAI-compatible third-party provider。
- Function calling。
- Structured output。

## RAG

- Qdrant 或 Weaviate。
- OpenAI embeddings 或 sentence-transformers。
- Hybrid search。
- Reranking。
- Citation-aware answer generation。

## Database

- PostgreSQL。
- Redis。

## Data Pipeline

- Python ETL。
- pandas。
- SEC EDGAR API。
- FRED API。

## Async / Workflow

- Celery 或 RQ。
- Redis Queue。

## LLMOps

- LangSmith 或 MLflow。
- Custom evaluation scripts。
- Prompt regression tests。

## Monitoring

- Prometheus。
- Grafana。
- OpenTelemetry。
- Cost logs。

## DevOps

- Docker Compose。
- GitHub Actions。
- Optional Kubernetes。

## Frontend

- Streamlit：最快 delivery。
- React + TypeScript：更強 full-stack signal。

目前這個 repo 使用 React + TypeScript。

## Data Sources

## 金融文件

SEC EDGAR APIs：

https://www.sec.gov/search-filings/edgar-application-programming-interfaces

用途：

- 10-K。
- 10-Q。
- Annual reports。
- Company announcements。
- Filing metadata。

## 宏觀經濟資料

FRED API：

https://fred.stlouisfed.org/docs/api/fred/

用途：

- Interest rates。
- CPI。
- GDP。
- Unemployment rate。
- Yield curve。

## 公司財務 Facts

SEC Company Facts API，同樣來自 SEC EDGAR。

用途：

- Revenue。
- Net income。
- Assets。
- Liabilities。
- Equity。
- Shares。
- Company comparison。

## 自製企業政策文件

這些 policy docs 很重要，因為它們能展示 enterprise governance、compliance QA、policy-grounded RAG 和 auditability。

建議建立：

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

## MVP Scope

MVP 不應一開始做太大。目標是先建立穩定的 Senior AI Engineer project，再逐步升級成 Solution Architect portfolio。

MVP 建議包含：

1. 可 ingest SEC filings。
2. 可 ingest FRED macro data。
3. 可 ingest internal policy docs。
4. 有 Qdrant vector search。
5. 有 PostgreSQL 儲存 structured financial data。
6. 有 LangGraph router。
7. 有 3 個 agents：
   - Document Agent。
   - Macro Agent。
   - Policy Agent。
8. 有 FastAPI endpoint。
9. 有 frontend UI。
10. 有 basic evaluation + request logging。

## Advanced Scope

完成 MVP 後再加入：

1. SQL Analytics Agent。
2. Role-based access control。
3. Prompt injection detection。
4. PII masking。
5. Cost dashboard。
6. Latency dashboard。
7. Model fallback。
8. Batch evaluation。
9. Docker Compose 一鍵啟動。
10. Architecture Pack Markdown / PDF。

這部分會讓專案從 engineering demo 升級成 Level 5 Solution Architect project。

## 2-3 Month Roadmap

## Week 1-2：Project Skeleton

建立 repo structure：

```text
enterprise-financial-intelligence-agent/
  backend/
  frontend/
  data/
  docs/
  evals/
  infra/
  notebooks/
```

完成：

- FastAPI skeleton。
- PostgreSQL。
- Qdrant。
- Docker Compose。
- Basic health check。

## Week 3-4：Data and RAG

完成：

- SEC filing ingestion。
- Policy document ingestion。
- Chunking。
- Embeddings。
- Qdrant indexing。
- RAG answer with citation。

練習：

- 比較 chunk size。
- 比較 embedding model。
- 比較 top-k。
- 比較 reranking 對答案品質的影響。

## Week 5-6：Agentic Workflow

完成：

- LangGraph router。
- Document Agent。
- Macro Agent。
- Policy Agent。
- Multi-step answer generation。

練習：

- 讓一個問題可以同時查 SEC 文件與 FRED 數據。
- Example：

```text
Analyze how rising interest rates may affect Apple's revenue and valuation risk.
```

## Week 7-8：Production Engineering

完成：

- Request logging。
- Error handling。
- Retry。
- Timeout。
- Model fallback。
- PII masking。
- Basic RBAC。

練習：

- Bad input。
- Prompt injection。
- Very long documents。
- API failure。

## Week 9-10：LLMOps / Evaluation

完成：

- Evaluation dataset。
- Retrieval score。
- Faithfulness score。
- Latency。
- Token cost。
- LangSmith / MLflow logging。

練習：

- 建立 50-100 條 evaluation questions。
- 分成：
  - factual。
  - analytical。
  - compliance。
  - multi-agent。

## Week 11-12：Architect Deliverables

完成：

- Architecture diagram。
- Data flow diagram。
- Security design。
- Cost estimate。
- Risk register。
- Deployment roadmap。
- README。
- Demo script。

這一階段最重要，因為它會讓 project 從工程 demo 升級成 Solution Architect portfolio。

## Final Deliverables

最後應該有：

1. GitHub Repo。
2. Live 或 local demo。
3. README。
4. Architecture Document。
5. API documentation。
6. Evaluation Report。
7. Cost & Latency Report。
8. Security & Governance Document。
9. 5-8 分鐘 Demo Video script。
10. Interview talking points。

## Interview Selling Points

最能打動面試官的功能：

1. 問題回答有引用來源。
2. Agent 會自動選工具。
3. 回答會顯示用了哪些資料。
4. 有 evaluation report。
5. 有 token / cost / latency dashboard。
6. 有 prompt injection / PII protection。
7. 有 architecture diagram。
8. 有 business value explanation。

## Sprint 1 Priority

第一個 Sprint 建議：

```text
FastAPI + Qdrant + PostgreSQL + SEC ingestion + basic RAG answer
```

先不要做 complex agent orchestration。

先打穩基礎：

- Data ingestion。
- Retrieval。
- Citations。
- Stable answer format。
- Basic request logging。

Sprint 1 完成後，再加 LangGraph routing。這樣 project 會比較穩，不會一開始就在 agent orchestration 裡卡住。
