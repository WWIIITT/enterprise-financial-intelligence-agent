# Observability Dashboard

## Definition

The Observability Dashboard summarizes operational data from request logs, evaluation runs, and security audits.

## Why It Exists In Aurelia Ledger

Operators need to know which agents are used, how long requests take, whether evaluations are passing, and how often security guardrails trigger.

## How It Works In This Repo

- Request logs track selected agent, latency, sources count, and estimated cost.
- Evaluation runs track suite results.
- Security audits track risk level and action.
- `/api/observability/summary` aggregates the latest state.
- The React dashboard displays compact metrics and distributions.

## Design Tradeoffs

- Custom PostgreSQL observability is simple and portfolio-friendly.
- Prometheus and Grafana would be stronger for production.
- Empty database states return stable summaries instead of failing.

## Failure Modes

- PostgreSQL logs are not a full metrics backend.
- Long-term retention policy is not implemented.
- High-cardinality metrics need careful production design.

## Interview Explanation

Observability turns the project from a chatbot into an operable system. It shows what happened, not just what the user saw.
