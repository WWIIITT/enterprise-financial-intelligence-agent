# Architecture

## System Goal

Aurelia Ledger is an enterprise financial intelligence platform. It combines document research, macroeconomic analysis, structured analytics, policy compliance, and multi-agent orchestration into a traceable AI workflow.

## High-Level Architecture

```text
React Frontend
  |
FastAPI Gateway
  |
Auth / RBAC / Request Logger
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

The in-memory store remains only as a local development guard. Qdrant is the primary vector retrieval backend when configured.

## LangGraph Workflow

```text
/api/chat
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

## Target Data Flow

- SEC filings are fetched from EDGAR, saved as raw files, parsed, chunked, embedded, and indexed in Qdrant.
- Policy documents are written as Markdown or PDF, chunked, embedded, and indexed in Qdrant.
- Company financial facts are stored in PostgreSQL for SQL analytics.
- SQL analytics requests use predefined metric templates and never accept raw SQL.
- FRED macro series are fetched through the FRED API and cached for repeat analysis.
- Every chat request records route, sources, latency, token usage, estimated cost, and errors.

## Governance Design

Planned governance controls:

- PII masking before model calls.
- Prompt injection detection for retrieved documents and user input.
- Role-based access control for restricted data.
- Audit logs for research, compliance, and client-facing workflows.
- Evaluation reports for faithfulness, retrieval quality, latency, and cost.
- Human approval paths for sensitive investment research outputs.
