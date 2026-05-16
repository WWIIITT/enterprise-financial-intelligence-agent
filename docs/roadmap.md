# Roadmap

## Current Stage

```text
Phase 2: RAG MVP
Current stage: demo-grade RAG is working; production-grade retrieval is next.
```

Current completion:

```text
Sprint 1: 80-90% completed
Sprint 2: Step 1 implemented; ready for provider verification
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
- Use Qdrant as the primary retrieval backend. Done when Qdrant and `EMBEDDING_MODEL` are configured.
- Store document metadata, chunk metadata, and request logs in PostgreSQL.
- Improve chunking strategy.
- Improve citation format.
- Add reranking. Initial lightweight reranking done.
- Add no-answer behavior when evidence is weak. Initial threshold behavior done.
- Improve answer synthesis.

Next task:

```text
Start Docker Desktop, verify Qdrant ingestion end to end, then improve chunking and citation quality
```

## Sprint 3: SEC EDGAR Live Ingestion

- SEC EDGAR connector.
- Ticker / CIK lookup.
- 10-K / 10-Q ingestion.
- Raw filing storage under `data/raw/`.
- Filing parser and text cleaner.
- Chunk + embed + index.
- SEC citations in answers.

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
