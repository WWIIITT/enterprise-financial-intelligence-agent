# Architecture

## System Goal

Aurelia Ledger is an enterprise financial intelligence platform. It combines document research, macroeconomic analysis, structured analytics, policy compliance, and multi-agent orchestration into a traceable AI workflow.

## High-Level Architecture

```text
React Frontend
  |
FastAPI Gateway
  |
Security Preflight / Request Logger
  |
LangGraph Orchestrator
  |
  |-- Document Research Agent -> Qdrant -> SEC filings
  |-- Macro Analysis Agent -> FRED API / cached macro table
  |-- SQL Analytics Agent -> PostgreSQL -> financial facts
  |-- Policy Compliance Agent -> Qdrant -> internal policies
  |-- Evaluation Engine -> eval dataset / scoring reports
  |
Observability Layer
  |-- token usage
  |-- latency
  |-- error rate
  |-- route trace
  |-- retrieval score
  |-- cost per request
```

## Current Implementation

The repo currently implements the core MVP foundation:

- FastAPI API shell.
- React + TypeScript frontend shell.
- Docker Compose for PostgreSQL, Qdrant, and Redis.
- Five enterprise-style internal policy documents.
- Provider embeddings with persistent Qdrant retrieval.
- SEC EDGAR live filing ingestion.
- FRED macro series analysis with PostgreSQL cache.
- SEC Company Facts ingestion with PostgreSQL financial facts.
- Safe SQL Analytics Agent with predefined query templates.
- LangGraph deterministic workflow orchestration.
- Evaluation suites for SEC, macro, orchestrator, and SQL routing.
- Deterministic Evaluation Engine with markdown/json reports.
- Deterministic Security / Governance preflight with PII masking and prompt injection blocking.
- Custom Observability Dashboard over request logs, evaluation runs, and security audits.

The in-memory store remains only as a local development guard. Qdrant is the primary vector retrieval backend when configured.

## LangGraph Workflow

```text
/api/chat
  |
security_preflight
  |
receive
  |
router_node
  |
  |-- policy -> Policy Compliance Agent -> policy RAG
  |-- document -> Document Research Agent -> SEC/document RAG
  |-- macro -> Macro Analysis Agent -> FRED/cache
  |-- sql -> SQL Analytics Agent -> PostgreSQL financial facts
  |-- macro_document -> Macro + Document route -> FRED/cache + SEC RAG
  |-- unknown -> fallback -> retrieval/no-answer safeguards
  |
respond with answer, sources, route trace, and metrics
```

Routing is deterministic in Sprint 5 to avoid extra LLM cost and keep evaluation repeatable.

## Security / Governance Flow

```text
/api/security/check or /api/chat
  |
detect PII and prompt injection patterns
  |
  |-- allow -> continue normal workflow
  |-- mask -> replace sensitive values, then route masked message
  |-- block -> return security-governance-agent response
  |
write audit record with message hash only when PostgreSQL is available
```

Sprint 8 uses deterministic guardrails. It does not call a moderation API and does not store raw sensitive text in security audit records.

## Observability Dashboard Flow

```text
/api/observability/summary
  |
read request_logs, evaluation_runs, security_audits
  |
aggregate latency, cost, route distribution, eval pass rate, and security actions
  |
return compact dashboard summary to React
```

Sprint 9 uses PostgreSQL as the observability store. Prometheus and Grafana remain optional future integrations.

## Evaluation Engine Flow

```text
/api/evals/run or /api/evals/report
  |
load JSON eval fixtures
  |
execute cases through LangGraph orchestrator
  |
score route, sources, citations, answer terms, latency, and forbidden terms
  |
record evaluation run in PostgreSQL when available
  |
return structured metrics
  |
optional report writer -> data/reports/evaluation-report.md/json
```

Sprint 7 uses deterministic scoring only. LLM-as-judge is intentionally out of scope for the MVP.

## Target Data Flow

- SEC filings are fetched from EDGAR, saved as raw files, parsed, chunked, embedded, and indexed in Qdrant.
- Policy documents are written as Markdown or PDF, chunked, embedded, and indexed in Qdrant.
- Company financial facts are stored in PostgreSQL for SQL analytics.
- SQL analytics requests use predefined metric templates and never accept raw SQL.
- FRED macro series are fetched through the FRED API and cached for repeat analysis.
- Every chat request records route, sources, latency, token usage, estimated cost, and errors.
- Security preflight records message hash, risk level, action, and finding count without raw PII.
- Observability summary reads request, evaluation, and security audit logs without creating new telemetry infrastructure.

## Governance Design

Current governance controls:

- PII masking before agent routing.
- Prompt injection detection for user input.
- Security audit records without raw sensitive text.
- Security evaluation suite for allow, mask, and block behavior.

Planned governance controls:

- Role-based access control for restricted data.
- Audit logs for research, compliance, and client-facing workflows.
- Evaluation reports for faithfulness, retrieval quality, latency, and cost.
- Human approval paths for sensitive investment research outputs.
