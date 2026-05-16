# Aurelia Ledger

**Enterprise Financial Intelligence Agent Platform**

Aurelia Ledger is a portfolio-grade AI agent platform that simulates how a financial services firm could automate internal research, compliance review, macro analysis, structured financial analytics, evaluation, and observability.

The project is designed to demonstrate Senior AI Engineer and AI Solution Architect capability through a working full-stack system, not just an isolated chatbot demo.

## Highlights

- Citation-aware RAG over internal policy documents and SEC filings
- Live SEC EDGAR 10-K / 10-Q ingestion with section-aware citations
- Macro Analysis Agent using FRED data with local sample fallback
- SQL Analytics Agent over SEC Company Facts stored in PostgreSQL
- LangGraph workflow orchestrator with deterministic agent routing
- Security preflight for PII masking and prompt-injection blocking
- Deterministic evaluation engine with markdown / JSON reports
- Observability dashboard over request, evaluation, and security logs
- Architecture, security, cost, deployment, and interview documentation
- VitePress knowledge site for sprint-by-sprint and concept-by-concept explanation

## System Architecture

```text
React Dashboard / Knowledge Site
  |
FastAPI Gateway
  |
Security Preflight
  |
LangGraph Orchestrator
  |
  |-- Policy Compliance Agent -> Qdrant -> Internal policies
  |-- Document Research Agent -> Qdrant -> SEC filings
  |-- Macro Analysis Agent -> PostgreSQL cache / FRED
  |-- SQL Analytics Agent -> PostgreSQL -> SEC Company Facts
  |-- Evaluation Engine -> JSON fixtures / reports
  |
Observability Layer
  |-- Request logs
  |-- Evaluation runs
  |-- Security audits
```

## Repository Structure

```text
backend/   FastAPI services, agents, models, tests, eval fixtures
frontend/  React + TypeScript operational dashboard
site/      VitePress public knowledge website
docs/      Architecture pack, roadmap, governance, cost, deployment docs
data/      Local policies, reports, raw/processed runtime artifacts
infra/     Docker Compose for PostgreSQL, Qdrant, and Redis
```

## Tech Stack

| Layer | Technologies |
| --- | --- |
| Backend | Python, FastAPI, Pydantic, SQLAlchemy |
| Agents | LangGraph, deterministic routing, OpenAI-compatible providers |
| Retrieval | Qdrant, provider embeddings, citation metadata |
| Data | PostgreSQL, Redis, SEC EDGAR, SEC Company Facts, FRED |
| Frontend | React, TypeScript, Vite, lucide-react |
| Docs site | VitePress, GitHub Pages |
| Evaluation | Deterministic JSON fixtures, markdown / JSON reports |
| Infrastructure | Docker Compose, GitHub Actions |

## Quick Start

### 1. Create Python Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt
```

### 2. Configure Environment

Create `.env` from `.env.example` and fill in provider values:

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

Do not commit `.env`.

### 3. Start Infrastructure

```powershell
docker compose -f infra\docker-compose.yml up -d
```

### 4. Start Backend

```powershell
cd backend
..\.venv\Scripts\python -m uvicorn app.main:app
```

Backend URL:

```text
http://localhost:8000
```

### 5. Start Frontend Dashboard

```powershell
cd frontend
npm install
npm run dev
```

Dashboard URL:

```text
http://localhost:5173
```

### 6. Start Knowledge Site

```powershell
cd site
npm install
npm run docs:dev
```

## Common Demo Flow

Run these from PowerShell after the backend is running.

### Health Check

```powershell
Invoke-RestMethod http://localhost:8000/health
```

### Ingest Policy Documents

```powershell
Invoke-RestMethod -Method Post http://localhost:8000/api/ingest/policy `
  -ContentType "application/json" `
  -Body '{"source":"all"}'
```

### Ingest Live SEC Filing

```powershell
Invoke-RestMethod -Method Post http://localhost:8000/api/ingest/sec `
  -ContentType "application/json" `
  -Body '{"source":"edgar","ticker":"AAPL","form_type":"10-K","filing_year":2025}'
```

### Ask A Policy Question

```powershell
Invoke-RestMethod -Method Post http://localhost:8000/api/chat `
  -ContentType "application/json" `
  -Body '{"message":"What does the AI Usage Policy say about approved use?"}'
```

### Ask A Company Risk Question

```powershell
Invoke-RestMethod -Method Post http://localhost:8000/api/chat `
  -ContentType "application/json" `
  -Body '{"message":"What risks are mentioned for Apple?"}'
```

### Run Full Evaluation

```powershell
Invoke-RestMethod -Method Post http://localhost:8000/api/evals/report `
  -ContentType "application/json" `
  -Body '{"suite":"all"}'
```

Generated reports:

```text
data/reports/evaluation-report.md
data/reports/evaluation-report.json
```

## API Surface

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Service health |
| `GET` | `/api/config/status` | Runtime configuration status |
| `POST` | `/api/chat` | Main LangGraph agent workflow |
| `POST` | `/api/security/check` | Standalone security guardrail check |
| `GET` | `/api/observability/summary` | Monitoring summary |
| `POST` | `/api/ingest/policy` | Ingest internal policy docs |
| `POST` | `/api/ingest/sec` | Ingest sample or live SEC filings |
| `POST` | `/api/ingest/company-facts` | Ingest SEC Company Facts |
| `GET` | `/api/macro/series/{series_id}` | Load FRED macro series |
| `POST` | `/api/macro/analyze` | Run macro analysis |
| `POST` | `/api/sql/analyze` | Run structured financial analytics |
| `POST` | `/api/evals/run` | Run deterministic eval suite |
| `POST` | `/api/evals/report` | Generate eval report |

## Validation

Run backend tests:

```powershell
.\.venv\Scripts\python -m pytest
```

Build frontend:

```powershell
cd frontend
npm run build
```

Build knowledge site:

```powershell
cd site
npm run docs:build
```

## Documentation

### Portfolio Deliverables

- [Architecture Pack](docs/architecture-pack.md)
- [Risk Register](docs/risk-register.md)
- [Cost Estimate](docs/cost-estimate.md)
- [Deployment Roadmap](docs/deployment-roadmap.md)
- [Security and Governance](docs/security-governance.md)
- [Demo Script](docs/demo-script.md)
- [Interview Talking Points](docs/interview-talking-points.md)
- [Latest Evaluation Report](data/reports/evaluation-report.md)

### Project Planning

- [Ultimate Goal](docs/ultimate-goal.md)
- [Roadmap](docs/roadmap.md)
- [Architecture](docs/architecture.md)
- [Data Sources](docs/data-sources.md)
- [Evaluation Plan](docs/evaluation-plan.md)

### Knowledge Website

The public learning site is implemented in [site/](site/index.md).

After GitHub Pages is enabled, the expected URL is:

```text
https://WWIIITT.github.io/enterprise-financial-intelligence-agent/
```

The site explains the project sprint by sprint, concept by concept, and workflow by workflow.

## Deployment Notes

The knowledge website is deployed through GitHub Pages using:

```text
.github/workflows/deploy-knowledge-site.yml
```

For the application stack, the current recommended deployment path is:

1. Local demo with Docker Compose
2. Single VM or container host
3. Managed cloud pilot
4. Production hardening with auth, RBAC, migration management, and dedicated monitoring

See [docs/deployment-roadmap.md](docs/deployment-roadmap.md) for details.

## Security Notes

- `.env` is ignored by Git and should never contain committed secrets
- Raw SQL input is not accepted
- Security audits store message hashes, not raw sensitive text
- Live SEC requests require an identifiable `SEC_USER_AGENT`
- FRED live data is optional; deterministic sample fallback supports local demos

## Project Status

The project has completed ten implementation and portfolio sprints:

```text
RAG MVP
Provider embeddings + Qdrant retrieval
SEC EDGAR ingestion
Macro Analysis Agent
LangGraph Orchestrator
SQL Analytics Agent
Evaluation Engine
Security / Governance Guardrails
Observability Dashboard
Architecture Pack + Knowledge Website
```
