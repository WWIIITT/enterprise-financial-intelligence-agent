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
