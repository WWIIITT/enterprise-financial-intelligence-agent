# Evaluation Reporting Flow

## Purpose

This workflow explains how evaluation suites become quality metrics and portfolio reports.

## Flow

```mermaid
flowchart TD
    Cases[JSON Eval Cases] --> Runner[Evaluation Runner]
    Runner --> Execution[Chat or Endpoint Execution]
    Execution --> Scoring[Deterministic Scoring]
    Scoring --> Metrics[Summary Metrics]
    Metrics --> Report[Markdown / JSON Report]
    Metrics --> DB[(Evaluation Run Record)]
```

## Metrics

- Pass rate
- Route accuracy
- Source coverage
- Citation score
- Answer term score
- Average latency
- P95 latency
- Hallucination-risk count

## What To Watch In A Demo

Generate `suite="all"` and open `data/reports/evaluation-report.md`.
