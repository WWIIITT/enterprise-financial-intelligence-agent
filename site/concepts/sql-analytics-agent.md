# SQL Analytics Agent

## Definition

The SQL Analytics Agent answers structured financial metric questions using safe query templates over PostgreSQL financial facts.

## Why It Exists In Aurelia Ledger

Some questions should not use RAG. Revenue trends and balance-sheet values are structured data problems and should be answered with controlled queries.

## How It Works In This Repo

- SEC Company Facts are ingested into PostgreSQL.
- Supported metrics map to predefined concepts.
- `/api/sql/analyze` accepts ticker, metric, period, and limit.
- Raw SQL input is never accepted.
- Chat questions with metric intent route to `sql-analytics-agent`.

## Design Tradeoffs

- Safe templates reduce injection risk.
- Deterministic analytics are easier to test.
- The approach supports fewer free-form questions than LLM-generated SQL.

## Failure Modes

- Unsupported metric.
- Missing company facts.
- Duplicate SEC facts for the same fiscal year.
- Concept mapping differs across companies.

## Interview Explanation

The important design choice is not just adding SQL. It is adding SQL safely, without letting the model generate arbitrary queries.
