# Roadmap

## Current Stage

```text
Phase 7: LLMOps / Evaluation Engine
Current stage: Sprint 7 deterministic evaluation engine is complete for MVP scope.
```

Current completion:

```text
Sprint 1: 80-90% completed
Sprint 2: core completed for MVP scope
Sprint 3: completed for MVP scope
Sprint 4: completed for MVP scope
Sprint 5: completed for MVP scope
Sprint 6: completed for MVP scope
Sprint 7: completed for MVP scope
```

## Sprint 1: Project Skeleton + RAG MVP Foundation

Goal:

```text
FastAPI + Docker services + basic RAG + citation answer + frontend demo
```

Completed:

- FastAPI backend skeleton.
- React + TypeScript frontend.
- Docker Compose for PostgreSQL, Qdrant, and Redis.
- `.env` config loading.
- `/health`.
- `/api/config/status`.
- `/api/ingest/policy`.
- `/api/ingest/sec`.
- `/api/chat`.
- Policy docs ingestion.
- SEC sample ingestion.
- Basic local RAG.
- Qdrant indexing when available.
- In-memory fallback.
- Citation-shaped response.
- Markdown-like answer rendering.
- Agent trace.
- Metrics placeholder.
- Browser ingestion buttons.
- System status panel.
- Responsive layout fixes.
- Enterprise-style policy documents.
- Backend tests and frontend build passing.

Status:

```text
Mostly complete.
```

## Sprint 2: Production-Grade RAG

Goal:

```text
real embeddings + persistent Qdrant + cleaner retrieval + better citations
```

Planned:

- Add real embedding client. Done.
- Support separate embedding provider API key/base URL. Done.
- Replace hash embedding with real embeddings. Done for Qdrant production path.
- Use Qdrant as the primary retrieval backend. Done.
- Store document metadata, chunk metadata, and request logs in PostgreSQL.
- Improve chunking strategy.
- Improve citation format.
- Add reranking. Initial lightweight reranking done.
- Add no-answer behavior when evidence is weak. Initial threshold behavior done.
- Improve answer synthesis.
- Validate Qdrant ingestion end to end with provider embeddings. Done.
- Route Apple risk retrieval to SEC evidence only. Done.

Status:

```text
Core complete for MVP scope. Retrieval quality hardening will continue in later sprints.
```

## Sprint 3: SEC EDGAR Live Ingestion

Next task:

```text
Implement SEC EDGAR live filing ingestion
```

- SEC EDGAR connector.
- Ticker / CIK lookup. Initial implementation done.
- Company submissions metadata lookup. Initial implementation done.
- 10-K / 10-Q ingestion. Initial latest-filing implementation done.
- Raw filing storage under `data/raw/sec/`. Done.
- Filing parser and text cleaner. Initial HTML/text cleaner plus common mojibake repair done.
- Chunk + embed + index. Done for live AAPL 10-K validation.
- SEC citations in answers with accession number, form type, filing date, and section. Initial implementation done.
- Risk questions prioritize Risk Factors evidence. Initial implementation done.

Completed hardening:

- SEC section parser with item boundary detection.
- Filing selection by year or accession number.
- UI controls for live SEC ingestion.
- Request throttling / retry behavior for SEC access.
- Deterministic SEC risk answer synthesis.
- SEC filing evaluation smoke cases.

## Sprint 4: Macro Analysis Agent

Goal:

```text
FRED macro data analysis + macro-aware chat routing
```

Completed:

- FRED client with live API path.
- Deterministic sample fallback when `FRED_API_KEY` is missing or FRED is unavailable.
- Supported series: `FEDFUNDS`, `CPIAUCSL`, `UNRATE`, `GDP`, `DGS10`.
- PostgreSQL macro observation cache.
- `GET /api/macro/series/{series_id}`.
- `POST /api/macro/analyze`.
- Macro-aware chat routing to `macro-analysis-agent`.
- Company + macro question support through `macro-document-orchestrator`.
- Frontend Macro Analysis controls.
- `macro-smoke` evaluation suite.

Status:

```text
Completed for MVP scope.
```

## Sprint 5: LangGraph Workflow Orchestrator

Goal:

```text
agent routing + multi-step trace
```

Completed:

- LangGraph `StateGraph` orchestrator.
- Deterministic router.
- Document Research route.
- Policy Compliance route.
- Macro Analysis route.
- Macro + Document route.
- Fallback route.
- Selected route in response.
- Unified multi-step trace.
- `orchestrator-smoke` evaluation suite.

Status:

```text
Completed for MVP scope.
```

## Sprint 6: SQL Analytics Agent

Goal:

```text
structured financial facts + safe SQL analytics
```

Completed:

- PostgreSQL financial facts schema.
- SEC Company Facts client.
- Deterministic AAPL sample fallback.
- `POST /api/ingest/company-facts`.
- `POST /api/sql/analyze`.
- Safe query templates with predefined metrics only.
- LangGraph `sql` route.
- Frontend SQL Analytics controls.
- `sql-smoke` evaluation suite.

Status:

```text
Completed for MVP scope.
```

## Sprint 7: LLMOps / Evaluation

Goal:

```text
deterministic scoring + evaluation report
```

Completed:

- Expanded eval case schema.
- Route accuracy scoring.
- Source coverage scoring.
- Citation correctness scoring.
- Answer term / faithfulness proxy scoring.
- Hallucination-risk flags.
- Average and p95 latency summary.
- `POST /api/evals/report`.
- Markdown and JSON report output under `data/reports/`.
- Evaluation run DB records.
- Frontend eval controls.

Status:

```text
Completed for MVP scope. Next step is Sprint 8 Security / Governance / Reliability.
```

## Sprint 8: Security / Governance / Reliability

- PII masking.
- Prompt injection detection.
- RBAC.
- Audit logs.
- Retry / timeout.
- Model fallback.
- Data retention policy.
- Human approval path.

## Sprint 9: Observability Dashboard

- Token usage.
- Latency.
- Error rate.
- Agent route.
- Retrieval score.
- Cost per request.
- Prometheus / Grafana or custom UI.

## Sprint 10: Architecture Pack / Portfolio Polish

- Architecture diagram.
- Data flow diagram.
- Security design.
- Cost estimate.
- Risk register.
- Deployment roadmap.
- Evaluation report.
- Demo script.
- Interview talking points.
