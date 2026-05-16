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
- MVP can start with cached sample macro data.
- Later phases should cache series into PostgreSQL for repeatable analysis.

## SEC Company Facts API

Use cases:

- Revenue.
- Net income.
- Assets and liabilities.
- Share count.
- Industry and company comparisons.

Implementation notes:

- Structured facts should be stored in PostgreSQL.
- SQL Analytics Agent should query this structured layer rather than raw filings.

## Internal Policy Documents

Source: self-authored sample documents in `data/policies/`.

Use cases:

- AI Usage Policy.
- Investment Research Review Policy.
- Data Privacy and PII Handling Policy.
- Model Risk Management Policy.
- Client Communication Policy.

These documents are important for demonstrating enterprise governance, compliance QA, policy-grounded RAG, and auditability.
