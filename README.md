# Aurelia Ledger

**Enterprise Financial Intelligence Agent Platform**

Aurelia Ledger 是一個 Level 4 / Level 5 portfolio project，目標是展示 Senior AI Engineer 與 AI Solution Architect 所需的能力：RAG、Agentic AI、金融資料整合、LLMOps、evaluation、安全治理、企業級架構設計與清晰文件交付。

本階段是 Phase 1 skeleton：建立可擴展的 FastAPI 後端、React + TypeScript 前端、環境設定、資料夾結構、文件與後續 roadmap。真正的 SEC / FRED / RAG / LangGraph 功能會在後續 phase 逐步加入。

## 專案定位

Aurelia Ledger 模擬金融公司內部的 AI intelligence platform。目標使用者包括投資研究、風險、合規、營運與管理層。

核心能力：

- 讀取 SEC filings、公司年報與內部政策文件
- 使用 RAG 回答問題並提供引用來源
- 使用 FRED 宏觀經濟資料輔助分析
- 使用 LangGraph orchestration 將問題 route 到不同 agent
- 透過 evaluation、metrics、logging、guardrails 降低 hallucination 與 production risk
- 產出 solution architecture、risk register、cost estimate 等 architect-level artifacts

## Job Description 對應能力

這個專案對應職缺中反覆出現的要求：

- `Python`, `FastAPI`, API integration
- `LLM API`, prompt engineering, OpenAI-compatible provider
- `RAG`, embeddings, vector database, citations
- `LangChain`, `LangGraph`, multi-agent workflow
- `PostgreSQL`, `Redis`, `Qdrant`
- `Docker`, CI/CD-ready structure
- `LLMOps`, evaluation, monitoring, token/cost/latency tracking
- `PII masking`, prompt injection checks, AI governance
- 金融資料、宏觀經濟資料、企業政策文件整合
- Solution architecture、business value、stakeholder communication

## Tech Stack

Backend:

- Python 3.11
- FastAPI
- Pydantic Settings
- OpenAI-compatible third-party LLM API
- PostgreSQL
- Redis
- Qdrant
- LangChain / LangGraph

Frontend:

- React
- TypeScript
- Vite
- npm
- lucide-react

Infrastructure:

- Docker Compose
- PostgreSQL
- Qdrant
- Redis

Planned LLMOps:

- LangSmith or MLflow
- Prometheus / Grafana
- Custom evaluation reports

## Local Setup

### 1. 建立 Python virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt
```

### 2. 設定環境變數

複製 `.env.example` 的格式到 `.env`，並填入你的第三方 OpenAI-compatible provider：

```env
LLM_API_KEY=
LLM_BASE_URL=https://your-openai-compatible-provider.example/v1
LLM_MODEL=
EMBEDDING_MODEL=
DATABASE_URL=postgresql+psycopg://aurelia:aurelia@localhost:5432/aurelia_ledger
QDRANT_URL=http://localhost:6333
REDIS_URL=redis://localhost:6379/0
FRED_API_KEY=
SEC_USER_AGENT=your-name your-email@example.com
```

`.env` 已加入 `.gitignore`，不要提交真實 API key。

### 3. 啟動後端

```powershell
cd backend
..\.venv\Scripts\python -m uvicorn app.main:app --reload
```

如 PowerShell 不接受上方路徑，使用：

```powershell
..\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

後端預設：

```text
http://localhost:8000
```

Health check:

```text
GET http://localhost:8000/health
```

### 4. 啟動前端

```powershell
cd frontend
npm install
npm run dev
```

前端預設：

```text
http://localhost:5173
```

### 5. 啟動基礎服務

```powershell
docker compose -f infra\docker-compose.yml up -d
```

包含：

- PostgreSQL: `localhost:5432`
- Qdrant: `localhost:6333`
- Redis: `localhost:6379`

## API Skeleton

目前 API 使用固定 response shape，方便前端與後續 LangGraph integration：

```text
GET  /health
POST /api/chat
GET  /api/config/status
POST /api/ingest/policy
POST /api/ingest/sec
GET  /api/macro/series/{series_id}
POST /api/evals/run
```

Chat response:

```json
{
  "answer": "string",
  "agent": "string",
  "sources": [],
  "trace": [],
  "metrics": {
    "latency_ms": 0,
    "estimated_cost_usd": 0,
    "tokens_input": 0,
    "tokens_output": 0
  }
}
```

## 2-3 個月 Roadmap

### Phase 1: Skeleton and documentation

- 建立 repo structure
- 建立 FastAPI backend skeleton
- 建立 React + TypeScript frontend skeleton
- 建立 `.env`, `.env.example`, `.gitignore`
- 建立 README 與 docs

### Phase 2: RAG MVP

- SEC EDGAR ingestion
- Policy document ingestion
- Chunking and embeddings
- Qdrant indexing
- Cited answer generation

### Phase 3: Agentic Workflow

- LangGraph router
- Document Research Agent
- Macro Analysis Agent
- Policy Compliance Agent
- SQL Analytics Agent

### Phase 4: Production Engineering / LLMOps

- Request logging
- Token, cost, latency tracking
- Evaluation dataset
- Prompt regression tests
- PII masking
- Prompt injection checks

### Phase 5: Architect Deliverables

- Architecture diagram
- Data flow diagram
- Security and governance document
- Cost estimate
- Risk register
- Demo script

## Data Sources

- SEC EDGAR APIs: company filings, 10-K, 10-Q, company facts  
  https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- FRED API: CPI, GDP, interest rates, unemployment and other macroeconomic data  
  https://fred.stlouisfed.org/docs/api/fred/
- Internal policy documents: sample files in `data/policies/`

## Interview Talking Points

- This is not only a chatbot. It is an enterprise AI platform skeleton with production concerns.
- The API response shape already reserves sources, trace and metrics for LLMOps.
- The architecture separates orchestration, RAG, services, agents and evaluation.
- The data sources map directly to finance and macro research workflows.
- The project roadmap shows how an MVP grows into a senior-level AI platform and architect-level solution package.
