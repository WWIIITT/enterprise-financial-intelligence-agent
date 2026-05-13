# Aurelia Ledger

**Enterprise Financial Intelligence Agent Platform**

Aurelia Ledger is a portfolio project for demonstrating Senior AI Engineer and AI Solution Architect capability. It simulates an internal financial intelligence platform that combines RAG, financial document analysis, macroeconomic data, policy compliance, agent routing, evaluation, monitoring, and governance documentation.

## Project Vision

The full product goal, module list, technology choices, roadmap, deliverables, and interview positioning are documented in [docs/ultimate-goal.md](docs/ultimate-goal.md).

## Current Status

This repo currently contains a working Phase 1 / Sprint 1 foundation:

- FastAPI backend with health, chat, ingestion, macro, config, and evaluation endpoints.
- React + TypeScript frontend skeleton.
- Docker Compose services for PostgreSQL, Qdrant, and Redis.
- Local policy documents in `data/policies/`.
- Basic local RAG ingestion and citation-shaped chat responses for development.
- Architecture, roadmap, data source, and evaluation documentation.

The first production-grade target is still:

```text
FastAPI + Qdrant + PostgreSQL + SEC ingestion + policy ingestion + citation-aware RAG
```

## Tech Stack

Backend:

- Python 3.11
- FastAPI
- Pydantic Settings
- SQLAlchemy
- PostgreSQL
- Qdrant
- Redis
- OpenAI-compatible LLM provider
- LangChain / LangGraph planned for orchestration

Frontend:

- React
- TypeScript
- Vite
- lucide-react

Infrastructure:

- Docker Compose
- PostgreSQL
- Qdrant
- Redis

## Local Setup

Create and activate the Python virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt
```

After activation, your terminal should show `(.venv)` before the prompt. To leave the virtual environment:

```powershell
deactivate
```

Create `.env` from `.env.example` and fill in local values:

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

Environment variable reference:

| Variable | Required now | Purpose |
| --- | --- | --- |
| `LLM_API_KEY` | Yes | API key for your OpenAI-compatible LLM provider. |
| `LLM_BASE_URL` | Yes | Base URL for the LLM provider, usually ending in `/v1`. |
| `LLM_MODEL` | Yes | Chat model used for answer generation. |
| `EMBEDDING_MODEL` | Not yet | Embedding model for production vector search. Current local RAG can run without it because it uses a development fallback. |
| `DATABASE_URL` | Yes | PostgreSQL connection string for metadata, chunks, and request logs. |
| `QDRANT_URL` | Yes | Qdrant vector database URL. |
| `REDIS_URL` | Later | Redis connection string for future queue/cache workflows. |
| `FRED_API_KEY` | Later | FRED API key for macroeconomic data ingestion. |
| `SEC_USER_AGENT` | Yes before live SEC ingestion | Identifiable SEC EDGAR user agent, normally `your-name your-email@example.com`. |

If you do not have an embedding model yet, leave `EMBEDDING_MODEL` empty for now:

```env
EMBEDDING_MODEL=
```

The current Sprint 1 development flow still works because local retrieval has a fallback path. Before production-grade Qdrant retrieval, choose an embedding model from your provider, for example an OpenAI-compatible embedding model such as `text-embedding-3-small` if your provider supports it.

Start infrastructure:

```powershell
docker compose -f infra\docker-compose.yml up -d
```

Run backend:

```powershell
cd backend
..\.venv\Scripts\python -m uvicorn app.main:app --reload
```

Backend URL:

```text
http://localhost:8000
```

Run frontend:

```powershell
cd frontend
npm install
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

## Run The Project End To End

Use PowerShell from the repo root.

### 1. Start Docker services

```powershell
docker compose -f infra\docker-compose.yml up -d
docker ps
```

Expected containers:

```text
aurelia-ledger-postgres
aurelia-ledger-qdrant
aurelia-ledger-redis
```

### 2. Activate Python environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If dependencies are missing:

```powershell
python -m pip install -r backend\requirements.txt
```

### 3. Run backend tests

```powershell
python -m pytest
```

Expected result:

```text
5 passed
```

### 4. Start FastAPI backend

Keep this terminal open:

```powershell
cd backend
..\.venv\Scripts\python -m uvicorn app.main:app --reload
```

Backend URL:

```text
http://localhost:8000
```

### 5. Verify backend from a second terminal

Open a second PowerShell terminal from the repo root:

```powershell
Invoke-RestMethod http://localhost:8000/health
Invoke-RestMethod http://localhost:8000/api/config/status
```

### 6. Optional API test: ingest policy documents

```powershell
Invoke-RestMethod -Method Post http://localhost:8000/api/ingest/policy `
  -ContentType "application/json" `
  -Body '{"source":"all"}'
```

Expected result:

```text
status            : completed
source_type       : policy
documents_indexed : 5
chunks_indexed    : greater than 5
vector_backend    : qdrant+in-memory
```

### 7. Optional API test: ingest sample SEC content

```powershell
Invoke-RestMethod -Method Post http://localhost:8000/api/ingest/sec `
  -ContentType "application/json" `
  -Body '{"source":"sample-sec-inline","ticker":"AAPL","content":"Apple reports revenue risk from foreign exchange, interest rates, product demand, supply chain constraints, and macroeconomic uncertainty."}'
```

### 8. Optional API test: RAG chat from PowerShell

```powershell
Invoke-RestMethod -Method Post http://localhost:8000/api/chat `
  -ContentType "application/json" `
  -Body '{"message":"What does the AI Usage Policy say about approved use?"}'
```

```powershell
Invoke-RestMethod -Method Post http://localhost:8000/api/chat `
  -ContentType "application/json" `
  -Body '{"message":"What risks are mentioned for Apple?"}'
```

The response should include:

```text
answer
agent
sources
trace
metrics
```

### 9. Start frontend

Open a third PowerShell terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

Use the Chat Console to ask a question. The browser UI calls `/api/chat` through the Vite proxy and displays the answer, sources, trace, and latency metrics.

### 10. Browser demo flow

In the browser:

1. Check `System Status`.
2. Confirm LLM Provider, PostgreSQL, Qdrant, Redis, and SEC User Agent are `Ready`.
3. `FRED API` can show `Later` during Sprint 1.
4. Click `Ingest Policy Docs`.
5. Click `Ingest SEC Sample`.
6. Ask:

```text
What does the AI Usage Policy say about approved use?
```

7. Click `Apple Risk` or ask:

```text
What risks are mentioned for Apple?
```

The UI should show the answer, citations, agent trace, latency, source count, ingestion status, and system configuration status. This flow no longer requires manual PowerShell ingestion for the demo.

## API

```text
GET  /health
POST /api/chat
GET  /api/config/status
POST /api/ingest/policy
POST /api/ingest/sec
GET  /api/macro/series/{series_id}
POST /api/evals/run
```

Example policy ingestion:

```powershell
Invoke-RestMethod -Method Post http://localhost:8000/api/ingest/policy `
  -ContentType "application/json" `
  -Body '{"source":"all"}'
```

Example chat:

```powershell
Invoke-RestMethod -Method Post http://localhost:8000/api/chat `
  -ContentType "application/json" `
  -Body '{"message":"What does the AI Usage Policy say about approved use?"}'
```

## Documentation

- [Ultimate Goal](docs/ultimate-goal.md)
- [Architecture](docs/architecture.md)
- [Data Sources](docs/data-sources.md)
- [Evaluation Plan](docs/evaluation-plan.md)
- [Roadmap](docs/roadmap.md)

## Notes

- `.env` is ignored by Git. Do not commit real API keys.
- Current local RAG uses an in-memory development store so the API can be tested before full PostgreSQL and Qdrant persistence is completed.
- You will manually commit and push to GitHub.
