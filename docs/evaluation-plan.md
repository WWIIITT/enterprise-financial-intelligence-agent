# Evaluation Plan

## Goal

Evaluation should measure more than whether the answer sounds good. Aurelia Ledger should evaluate retrieval quality, citation correctness, routing, faithfulness, latency, cost, and governance behavior.

## Evaluation Types

## Retrieval Evaluation

- Top-k recall.
- Citation correctness.
- Source coverage.
- No-answer behavior when evidence is missing.

## Answer Quality

- Faithfulness to retrieved sources.
- Completeness.
- Financial reasoning clarity.
- Hallucination rate.

## Agent Workflow

- Router accuracy.
- Tool selection correctness.
- Multi-step trace completeness.
- Failure fallback behavior.

## Production Metrics

- Latency p50 and p95.
- Token usage.
- Estimated cost per request.
- Error rate.
- Timeout rate.

## Governance Tests

- PII masking.
- Prompt injection refusal.
- Restricted data access behavior.
- Audit log completeness.

## Initial Eval Suites

- `smoke`: endpoint and response shape checks.
- `sec-smoke`: real SEC filing retrieval, citation, route, and unsupported-claim checks.
- `macro-smoke`: FRED/sample macro series, macro routing, and macro citation checks.
- `rag_factual`: factual questions requiring cited answers.
- `macro_analysis`: FRED-based macro reasoning.
- `policy_compliance`: internal policy QA.
- `multi_agent`: questions requiring more than one agent.

## SEC Filing Evaluation Cases

Sprint 3 adds deterministic SEC filing cases in `backend/app/evals/sec_filing_cases.json`.

Current checks:

- Apple risk factor questions route to `document-research-agent`.
- SEC answers cite accession number, form type, filing date, section, and chunk.
- Unsupported filing claims trigger no-answer behavior.
- Eval runner reports total cases, passed cases, pass rate, and latency.

## Macro Evaluation Cases

Sprint 4 adds deterministic macro cases in `backend/app/evals/macro_cases.json`.

Current checks:

- Inflation and CPI questions route to `macro-analysis-agent`.
- Macro answers cite FRED series IDs.
- Apple + interest rate questions produce company risk linkage.
- Macro evaluation reports total cases, passed cases, pass rate, and latency.
