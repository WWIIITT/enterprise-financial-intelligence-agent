# Interview Talking Points

## One-Minute Pitch

Aurelia Ledger is an enterprise financial intelligence agent platform. It combines SEC filing RAG, FRED macro analysis, SEC Company Facts SQL analytics, policy compliance, LangGraph orchestration, deterministic evaluation, security guardrails, and observability.

The project is designed to show that I can build not only an AI demo, but a traceable, governed, evaluable AI system suitable for financial enterprise workflows.

## Senior AI Engineer Signals

- Built provider-embedding RAG with Qdrant persistence.
- Implemented SEC EDGAR ingestion with filing selection, parsing, chunking, and citations.
- Added macro analysis with FRED API and cache fallback.
- Added safe SQL analytics over SEC Company Facts without raw SQL.
- Built LangGraph deterministic routing across document, policy, macro, SQL, and hybrid routes.
- Built deterministic evaluation suites and report generation.
- Added security preflight and observability APIs.

## AI Solution Architect Signals

- Mapped business workflows to agent capabilities.
- Separated unstructured RAG, structured analytics, macro data, and policy governance.
- Designed traceability through sources, citations, route traces, and request logs.
- Added risk register, cost estimate, deployment roadmap, and governance documentation.
- Made explicit tradeoffs around deterministic routing, deterministic evaluation, and safe SQL templates.

## Key Tradeoffs

| Tradeoff | Decision | Reason |
| --- | --- | --- |
| Deterministic router vs LLM router | Deterministic router | Lower cost, repeatable eval, easier debugging |
| LLM-generated SQL vs templates | Safe templates | Prevent SQL injection and unstable queries |
| LLM-as-judge vs deterministic scoring | Deterministic scoring | No judge cost, predictable regression tests |
| Custom observability vs Grafana | Custom UI | Faster portfolio delivery with existing logs |
| Full RBAC vs placeholder governance | Documented future control | Keeps MVP focused while showing architecture thinking |

## Limitations To Acknowledge

- RBAC and SSO are not implemented yet.
- Evaluation is deterministic and should be expanded with human review or LLM-as-judge later.
- Observability is custom and not yet Prometheus/Grafana-based.
- SQL analytics supports predefined metrics rather than arbitrary questions.
- Model fallback and full production deployment automation are future work.

## What I Would Build Next

- RBAC with role-specific access to filings, policies, and analytics.
- Alembic migrations for production schema management.
- Batch ingestion workers with queue-based retries.
- Model/provider fallback with health checks.
- Human approval workflow for client-facing outputs.
- Prometheus metrics and Grafana dashboards.
- More advanced retrieval evaluation with labeled datasets.

## STAR Examples

## Situation

Financial analysts need answers that combine SEC filings, macro data, structured metrics, and internal policy constraints.

## Task

Build a portfolio-grade platform that demonstrates enterprise AI engineering and architecture thinking.

## Action

Implemented ingestion, RAG, macro analysis, SQL analytics, LangGraph routing, deterministic evaluation, security guardrails, observability, and architecture documentation.

## Result

The platform can ingest live SEC filings, answer cited research questions, analyze macro trends, query structured financial facts, enforce security preflight, run evaluation suites, and expose operational metrics.

## Strong Interview Answers

**Why deterministic routing first?**

Because the first goal was reliability and evaluability. Deterministic routing keeps cost low, makes failures explainable, and gives a stable baseline before adding LLM-based routing.

**Why avoid LLM-generated SQL?**

Financial data queries need safety and repeatability. Predefined templates avoid SQL injection and make tests deterministic.

**How do you reduce hallucination risk?**

Use source-grounded retrieval, citations, no-answer behavior, deterministic answer synthesis for sensitive flows, and evaluation checks for answer terms and citation coverage.

**How does this become production-ready?**

Add RBAC, SSO, migrations, queue-based ingestion, provider fallback, retention policy, approval workflow, and production observability.
