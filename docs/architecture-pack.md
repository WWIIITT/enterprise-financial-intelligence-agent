# Architecture Pack

## Executive Summary

Aurelia Ledger is an enterprise financial intelligence platform that simulates how a financial services firm could combine document research, macroeconomic analysis, structured financial analytics, policy compliance, security guardrails, evaluation, and observability into one AI-assisted research workflow.

The project is designed to demonstrate two complementary capabilities:

- Senior AI Engineer: building reliable RAG, data ingestion, agent routing, deterministic evaluation, and production-style APIs.
- AI Solution Architect: connecting business goals, governance, risk controls, deployment planning, cost control, and operational monitoring.

## Business Context

Financial research and operations teams often need to answer questions that cross multiple data sources:

- SEC filings for company disclosures and risk factors.
- FRED macro data for economic context.
- SEC Company Facts for structured financial metrics.
- Internal policies for compliance and governance checks.

The platform models an internal assistant for research analysts, compliance reviewers, and operations teams. The system is intentionally traceable: responses include sources, route decisions, latency, and evaluation evidence.

## Current Capabilities

- Document Research Agent for SEC filings and policy RAG.
- Macro Analysis Agent for FRED or deterministic sample macro data.
- SQL Analytics Agent for safe structured financial facts.
- Policy Compliance Agent for internal governance documents.
- LangGraph Workflow Orchestrator for deterministic agent routing.
- Security preflight for PII masking and prompt injection blocking.
- Evaluation Engine with deterministic scoring and reports.
- Observability Dashboard over request logs, evaluation runs, and security audits.

## High-Level Architecture

```mermaid
flowchart TD
    UI[React Frontend] --> API[FastAPI Gateway]
    API --> Security[Security Preflight]
    Security --> Orchestrator[LangGraph Orchestrator]
    Orchestrator --> DocAgent[Document Research Agent]
    Orchestrator --> PolicyAgent[Policy Compliance Agent]
    Orchestrator --> MacroAgent[Macro Analysis Agent]
    Orchestrator --> SQLAgent[SQL Analytics Agent]
    DocAgent --> Qdrant[(Qdrant Vector DB)]
    PolicyAgent --> Qdrant
    MacroAgent --> MacroCache[(PostgreSQL Macro Cache)]
    MacroAgent --> FRED[FRED API]
    SQLAgent --> Facts[(PostgreSQL Financial Facts)]
    API --> Eval[Evaluation Engine]
    API --> Obs[Observability Summary]
    Obs --> Logs[(Request Logs / Eval Runs / Security Audits)]
```

## Agent Workflow

```mermaid
flowchart TD
    Request[User Question] --> Guardrail[Security Preflight]
    Guardrail -->|allow or mask| Router[LangGraph Router]
    Guardrail -->|block| SecurityAgent[Security Governance Agent]
    Router -->|policy| Policy[Policy Compliance Agent]
    Router -->|document| Document[Document Research Agent]
    Router -->|macro| Macro[Macro Analysis Agent]
    Router -->|sql| SQL[SQL Analytics Agent]
    Router -->|macro + company| Hybrid[Macro + Document Route]
    Router -->|unknown| Fallback[Fallback / No-Answer Safeguards]
    Policy --> Response[Cited Answer + Trace]
    Document --> Response
    Macro --> Response
    SQL --> Response
    Hybrid --> Response
    Fallback --> Response
    SecurityAgent --> Response
```

## Data Flow

```mermaid
flowchart LR
    SEC[SEC EDGAR Filings] --> SECIngest[SEC Ingestion]
    Policies[Internal Policies] --> PolicyIngest[Policy Ingestion]
    CompanyFacts[SEC Company Facts] --> FactIngest[Financial Facts Ingestion]
    FRED[FRED Series] --> MacroService[Macro Service]
    SECIngest --> Chunking[Parse / Clean / Chunk]
    PolicyIngest --> Chunking
    Chunking --> Embed[Provider Embeddings]
    Embed --> Qdrant[(Qdrant)]
    FactIngest --> Postgres[(PostgreSQL)]
    MacroService --> Postgres
```

## Evaluation And Observability Flow

```mermaid
flowchart TD
    EvalAPI[/api/evals/run or report/] --> Fixtures[JSON Eval Fixtures]
    Fixtures --> ChatFlow[Chat / Endpoint Execution]
    ChatFlow --> Scoring[Deterministic Scoring]
    Scoring --> EvalRecord[(Evaluation Runs)]
    Scoring --> Reports[Markdown / JSON Reports]
    Requests[Chat Requests] --> RequestLogs[(Request Logs)]
    Security[Security Checks] --> SecurityAudits[(Security Audits)]
    RequestLogs --> ObsAPI[/api/observability/summary/]
    EvalRecord --> ObsAPI
    SecurityAudits --> ObsAPI
    ObsAPI --> Dashboard[React Observability Panel]
```

## Key Design Decisions

| Decision | Rationale | Tradeoff |
| --- | --- | --- |
| Deterministic routing before LLM routing | Repeatable, low cost, easy to evaluate | Less flexible than LLM-based intent classification |
| Provider embeddings with Qdrant | Persistent vector search and realistic RAG architecture | Requires embedding configuration and collection management |
| Safe SQL templates only | Avoids SQL injection and unstable generated SQL | Less flexible than free-form analytics questions |
| Deterministic evaluation | No LLM judge cost, predictable CI behavior | Only a proxy for semantic quality |
| Security preflight before routing | Prevents risky requests from reaching tools | Rule-based detection will miss some attacks |
| Custom observability dashboard | Fast portfolio value using existing PostgreSQL logs | Less comprehensive than Prometheus/Grafana |

## Production Gaps

- Authentication and RBAC are not fully implemented.
- LLM answer generation is intentionally limited in several paths to reduce cost and hallucination risk.
- Evaluation uses deterministic checks rather than human or LLM-as-judge review.
- Observability is stored in PostgreSQL, not a dedicated metrics backend.
- No Alembic migration framework is included yet.

## Recommended Next Architecture Steps

- Add SSO and role-aware access policies.
- Add formal migration management.
- Add batch ingestion jobs and retry queues.
- Add model fallback and provider health checks.
- Add Prometheus metrics for production deployment.
- Add human approval workflow for external research distribution.
