# Roadmap

## Current Stage

```text
Phase 3: SEC EDGAR Live Ingestion
Current stage: Sprint 2 production-grade RAG core is complete; live SEC ingestion is next.
```

Current completion:

```text
Sprint 1: 80-90% completed
Sprint 2: core completed for MVP scope
Sprint 3: started
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
- Filing parser and text cleaner. Initial HTML/text cleaner done.
- Chunk + embed + index.
- SEC citations in answers with accession number, form type, filing date, and section. Initial implementation done.

Next hardening:

- Improve SEC section parsing beyond simple keyword inference.
- Add filing selection by year or accession number.
- Add UI controls for live SEC ingestion.
- Add request throttling / retry behavior for SEC access.

## Sprint 4: Macro Analysis Agent

- FRED API connector.
- CPI, GDP, unemployment, interest rates.
- Cached macro series.
- Macro summary generation.
- Company risk + macro question support.

## Sprint 5: LangGraph Workflow Orchestrator

- LangGraph router.
- Document Research Agent.
- Policy Compliance Agent.
- Macro Analysis Agent.
- Later SQL Analytics Agent.
- Selected route in response.
- Multi-agent trace.

## Sprint 6: SQL Analytics Agent

- PostgreSQL financial facts schema.
- SEC Company Facts ingestion.
- SQL query tool.
- Safe SQL generation.
- Financial metrics analysis.
- Company / sector comparison.

## Sprint 7: LLMOps / Evaluation

- Eval dataset.
- Retrieval recall.
- Citation correctness.
- Faithfulness score.
- Hallucination checks.
- Latency tracking.
- Token / cost tracking.
- Batch eval report.

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
