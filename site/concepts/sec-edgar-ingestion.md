# SEC EDGAR Ingestion

## Definition

SEC EDGAR ingestion downloads company filings such as 10-K and 10-Q reports, cleans the filing text, parses sections, chunks the content, embeds the chunks, and indexes them for document research.

## Why It Exists In Aurelia Ledger

SEC filings are primary-source evidence for company risk, business strategy, financial disclosures, and management discussion.

## How It Works In This Repo

- Ticker is resolved to CIK.
- Filing selection supports latest form, filing year, or accession number.
- SEC requests use a configured `SEC_USER_AGENT`.
- HTML is cleaned and common encoding issues are repaired.
- Section parser assigns labels such as Business, Risk Factors, MD&A, and Market Risk.
- Chunks are indexed with SEC citation metadata.

## Design Tradeoffs

- Deterministic parsing is transparent and testable.
- SEC throttling and retry behavior reduce external API fragility.
- The parser is not a full XBRL or filing structure engine.

## Failure Modes

- Missing SEC user agent.
- Ticker or filing not found.
- SEC rate limiting.
- Filing text is too noisy or section headings are unusual.

## Interview Explanation

The SEC connector shows the system can ingest real regulatory documents, not just curated local samples.
