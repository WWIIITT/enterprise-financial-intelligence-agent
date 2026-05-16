# Data Sources

## SEC EDGAR APIs

Source: https://www.sec.gov/search-filings/edgar-application-programming-interfaces

Use cases:

- 10-K and 10-Q filings.
- Annual reports and company announcements.
- Company Facts API for structured financial metrics.
- XBRL-derived financial facts.

Implementation notes:

- `SEC_USER_AGENT` must contain an identifiable name and email.
- Raw files should be stored under `data/raw/`.
- Processed files should be stored under `data/processed/`.
- SEC ingestion should support a local sample fallback for demos.
- Sprint 3 live ingestion uses SEC ticker mapping, company submissions metadata, and filing archive documents.
- Live filing citations should include ticker, form type, filing date, accession number, inferred section, and chunk number.
- Filing selection supports accession number, filing year plus form type, or latest form type.
- SEC requests use bounded retry and a small delay to reduce transient failure and rate-limit risk.

## FRED API

Source: https://fred.stlouisfed.org/docs/api/fred/

Use cases:

- Interest rates.
- CPI.
- GDP.
- Unemployment rate.
- Yield curve and macro risk indicators.

Implementation notes:

- Live API access requires `FRED_API_KEY`.
- Sprint 4 supports live FRED observations when `FRED_API_KEY` is configured.
- If the key is missing or FRED is unavailable, the app uses deterministic sample macro data for local demo and tests.
- Supported MVP series:
  - `FEDFUNDS`: Federal Funds Effective Rate.
  - `CPIAUCSL`: Consumer Price Index.
  - `UNRATE`: Unemployment Rate.
  - `GDP`: Gross Domestic Product.
  - `DGS10`: 10-Year Treasury Constant Maturity Rate.
- Macro observations are cached in PostgreSQL for repeatable analysis.
- `/api/macro/series/{series_id}` returns observations, summary, source, units, and cache status.
- `/api/macro/analyze` combines selected macro series into a deterministic macro summary.
- Macro-aware chat routing sends inflation, interest rate, unemployment, GDP, treasury, and yield questions to the Macro Analysis Agent.

## SEC Company Facts API

Use cases:

- Revenue.
- Net income.
- Assets and liabilities.
- Share count.
- Industry and company comparisons.

Implementation notes:

- Sprint 6 stores structured facts in PostgreSQL.
- The SQL Analytics Agent queries this structured layer rather than raw filings.
- Live Company Facts requests require `SEC_USER_AGENT`.
- If SEC live access is unavailable, the service uses deterministic AAPL sample facts for demo and tests.
- Supported MVP metrics:
  - revenue.
  - net income.
  - assets.
  - liabilities.
  - cash.
  - operating cash flow.
  - shares outstanding.
- `/api/ingest/company-facts` ingests structured company facts.
- `/api/sql/analyze` runs safe predefined query templates.
- Raw SQL input and LLM-generated SQL are intentionally out of scope for Sprint 6.

## Internal Policy Documents

Source: self-authored sample documents in `data/policies/`.

Use cases:

- AI Usage Policy.
- Investment Research Review Policy.
- Data Privacy and PII Handling Policy.
- Model Risk Management Policy.
- Client Communication Policy.

These documents are important for demonstrating enterprise governance, compliance QA, policy-grounded RAG, and auditability.
