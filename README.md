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
- Sprint 2 provider embeddings for persistent Qdrant retrieval.
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
EMBEDDING_API_KEY=
EMBEDDING_BASE_URL=https://your-openai-compatible-provider.example/v1
EMBEDDING_MODEL=text-embedding-3-small
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
| `EMBEDDING_API_KEY` | Optional | API key for a separate embedding provider. If empty, `LLM_API_KEY` is reused. |
| `EMBEDDING_BASE_URL` | Optional | Base URL for a separate embedding provider. If empty, `LLM_BASE_URL` is reused. Prefer `/v1`, not `/v1/embeddings`. |
| `EMBEDDING_MODEL` | Yes for Sprint 2 RAG | Embedding model for production Qdrant vector search, for example `text-embedding-3-small`. |
| `DATABASE_URL` | Yes | PostgreSQL connection string for metadata, chunks, and request logs. |
| `QDRANT_URL` | Yes | Qdrant vector database URL. |
| `REDIS_URL` | Later | Redis connection string for future queue/cache workflows. |
| `FRED_API_KEY` | Later | FRED API key for macroeconomic data ingestion. |
| `SEC_USER_AGENT` | Yes before live SEC ingestion | Identifiable SEC EDGAR user agent, normally `your-name your-email@example.com`. |

For Sprint 2 RAG, set `EMBEDDING_MODEL` to an embedding model supported by your OpenAI-compatible provider:

```env
EMBEDDING_BASE_URL=https://your-openai-compatible-provider.example/v1
EMBEDDING_MODEL=text-embedding-3-small
```

Do not use a rerank model such as `qwen3-rerank` for `EMBEDDING_MODEL`. Qdrant needs a text embedding model to create vectors. If `EMBEDDING_MODEL` is empty while Qdrant is running, ingestion and chat will return a clear API error because Sprint 2 persistent retrieval requires real embeddings.

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

If Windows blocks port `8000` with `[WinError 10013]`, use port `8001`:

```powershell
cd backend
..\.venv\Scripts\python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

Backend fallback URL:

```text
http://localhost:8001
```

Run frontend:

```powershell
cd frontend
npm install
npm run dev
```

If the backend is running on port `8001`, start frontend with:

```powershell
cd frontend
$env:VITE_API_TARGET="http://localhost:8001"
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

Windows port fallback:

```powershell
cd backend
..\.venv\Scripts\python -m uvicorn app.main:app
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
vector_backend    : qdrant-provider-embeddings
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

## Sprint 2 RAG Runbook

Sprint 2 uses provider embeddings and Qdrant as the primary retrieval backend.

1. Confirm `.env` has these values:

```env
LLM_API_KEY=your-provider-key
LLM_BASE_URL=https://your-openai-compatible-provider.example/v1
LLM_MODEL=your-chat-model
EMBEDDING_API_KEY=your-provider-key
EMBEDDING_BASE_URL=https://your-openai-compatible-provider.example/v1
EMBEDDING_MODEL=text-embedding-3-small
QDRANT_URL=http://localhost:6333
```

2. Start infrastructure:

```powershell
docker compose -f infra\docker-compose.yml up -d
```

3. Start the backend:

```powershell
cd backend
..\.venv\Scripts\python -m uvicorn app.main:app --reload
```

4. Ingest policy and SEC sample from the browser, or use PowerShell:

```powershell
Invoke-RestMethod -Method Post http://localhost:8000/api/ingest/policy `
  -ContentType "application/json" `
  -Body '{"source":"all"}'
```

```powershell
Invoke-RestMethod -Method Post http://localhost:8000/api/ingest/sec `
  -ContentType "application/json" `
  -Body '{"source":"sample-sec-inline","ticker":"AAPL","content":"Apple reports revenue risk from foreign exchange, interest rates, product demand, supply chain constraints, and macroeconomic uncertainty."}'
```

5. Test cited chat:

```powershell
Invoke-RestMethod -Method Post http://localhost:8000/api/chat `
  -ContentType "application/json" `
  -Body '{"message":"What risks are mentioned for Apple?"}'
```

Common Sprint 2 issues:

- `EMBEDDING_MODEL is required`: add a provider-supported embedding model to `.env`.
- `Embedding provider request failed`: check `EMBEDDING_API_KEY`, `EMBEDDING_BASE_URL`, `EMBEDDING_MODEL`, and whether your provider supports embeddings.
- `EMBEDDING_MODEL appears to be a reranking model`: choose a model tagged as text embedding, not rerank.
- `Qdrant collection vector size is ...`: your existing Qdrant collection was created with another embedding dimension. Recreate the Docker volume or reset the collection, then ingest again.

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
- Sprint 2 uses provider embeddings and Qdrant for persistent retrieval when Qdrant is running. The in-memory store remains only as a development/test guard.
- You will manually commit and push to GitHub.
