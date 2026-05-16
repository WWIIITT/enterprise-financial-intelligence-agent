# FRED Macro Agent

## Definition

The Macro Analysis Agent loads macroeconomic time series from FRED or deterministic sample data, summarizes recent observations, and cites the series used.

## Why It Exists In Aurelia Ledger

Company risk often depends on macro context. Interest rates, inflation, unemployment, GDP, and treasury yields can all affect valuation, demand, and investor sentiment.

## How It Works In This Repo

- Supported series include `FEDFUNDS`, `CPIAUCSL`, `UNRATE`, `GDP`, and `DGS10`.
- The service uses FRED when `FRED_API_KEY` is configured.
- Sample fallback keeps local demos and tests stable.
- Observations are cached in PostgreSQL.
- Macro questions route to `macro-analysis-agent`.
- Company-plus-macro questions can route to `macro-document-orchestrator`.

## Design Tradeoffs

- Deterministic summaries avoid extra LLM cost.
- Sample fallback improves demo reliability.
- The current trend logic is simple and explainable.

## Failure Modes

- FRED API key missing.
- Series unavailable.
- Cached data stale.
- Macro context overgeneralized without company-specific evidence.

## Interview Explanation

The macro agent demonstrates multi-source reasoning: a user can combine external economic indicators with company disclosures.
