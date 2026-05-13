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

The repo currently implements the first development foundation:

- FastAPI API shell.
- React + TypeScript frontend shell.
- Docker Compose for PostgreSQL, Qdrant, and Redis.
- Local policy documents.
- In-memory development RAG store for ingestion and citation-shaped chat responses.

The in-memory store is intentionally temporary. It lets the API and frontend workflow be tested before persistent Qdrant and PostgreSQL integration is completed.

## Target Data Flow

- SEC filings are fetched from EDGAR, saved as raw files, parsed, chunked, embedded, and indexed in Qdrant.
- Policy documents are written as Markdown or PDF, chunked, embedded, and indexed in Qdrant.
- Company financial facts are stored in PostgreSQL for SQL analytics.
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
