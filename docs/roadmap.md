# Roadmap

## Phase 1: Skeleton

- FastAPI modular backend.
- React + TypeScript frontend.
- `.env` and `.env.example`.
- Docker Compose for PostgreSQL, Qdrant, and Redis.
- Documentation baseline.

Status: mostly complete.

## Phase 2: RAG MVP

- Policy document ingestion.
- SEC filing ingestion.
- Chunking strategy.
- Embeddings.
- Qdrant indexing.
- Citation-aware answer generation.
- PostgreSQL metadata and request logging.

Status: in progress. Current implementation includes browser-triggered ingestion, enterprise-style policy documents, Qdrant-backed indexing when available, and a local in-memory development RAG fallback. Production-grade embeddings and live SEC ingestion are next.

## Phase 3: Agentic Workflow

- LangGraph router.
- Document Research Agent.
- Macro Analysis Agent.
- Policy Compliance Agent.
- SQL Analytics Agent.
- Multi-agent trace in frontend.

## Phase 4: LLMOps and Reliability

- Evaluation dataset.
- Prompt regression tests.
- Token and cost tracking.
- Latency and error metrics.
- PII masking.
- Prompt injection checks.
- Retry and fallback policies.

## Phase 5: Architect Package

- Architecture diagram.
- Data flow diagram.
- Cost estimate.
- Risk register.
- Security and governance plan.
- Demo script.
- Interview talking points.
