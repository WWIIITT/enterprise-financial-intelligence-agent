# API Reference

## Core

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Service health check |
| `GET` | `/api/config/status` | Environment and service readiness |
| `POST` | `/api/chat` | Main agent workflow |

## Ingestion

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/api/ingest/policy` | Index internal policy documents |
| `POST` | `/api/ingest/sec` | Index sample or live SEC filings |
| `POST` | `/api/ingest/company-facts` | Index SEC Company Facts into PostgreSQL |

## Analysis

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/macro/series/{series_id}` | Load macro series observations |
| `POST` | `/api/macro/analyze` | Analyze macro context |
| `POST` | `/api/sql/analyze` | Analyze structured financial metrics |

## Governance And Operations

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/api/security/check` | Run deterministic security checks |
| `POST` | `/api/evals/run` | Run an evaluation suite |
| `POST` | `/api/evals/report` | Generate evaluation report |
| `GET` | `/api/observability/summary` | Load operational dashboard summary |
