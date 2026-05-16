# Risk Register

This risk register summarizes the main risks for an enterprise financial intelligence agent platform and how Aurelia Ledger currently mitigates them.

| Risk | Category | Impact | Likelihood | Mitigation | Current Status |
| --- | --- | --- | --- | --- | --- |
| Hallucinated financial claims | AI quality | High | Medium | Citation-aware RAG, deterministic synthesis, no-answer safeguards, evaluation cases | Partially mitigated |
| Stale SEC filings | Data freshness | High | Medium | Live EDGAR ingestion, filing date and accession citations | Partially mitigated |
| FRED API outage | External dependency | Medium | Medium | Deterministic sample fallback and macro cache | Mitigated for demo |
| SEC API throttling or failure | External dependency | Medium | Medium | SEC user agent, bounded retry, throttling | Partially mitigated |
| Embedding model drift | Retrieval quality | Medium | Medium | Model metadata and dimension checks for Qdrant | Partially mitigated |
| Prompt injection | Security | High | High | Security preflight and prompt injection blocking | Initial mitigation |
| PII leakage | Security / privacy | High | Medium | PII masking and security audit records without raw text | Initial mitigation |
| Raw SQL misuse | Security | High | Low | No raw SQL input, predefined SQL analytics templates | Mitigated |
| Over-reliance on deterministic routing | Product quality | Medium | Medium | Route evaluation suite and clear trace output | Accepted for MVP |
| Vendor lock-in | Architecture | Medium | Medium | OpenAI-compatible interfaces and deterministic fallbacks | Partially mitigated |
| Cost growth from embeddings or chat calls | Cost | Medium | Medium | Caching, deterministic synthesis, limited top-k | Partially mitigated |
| Weak evaluation coverage | LLMOps | Medium | Medium | SEC, macro, SQL, orchestrator, security, and observability smoke suites | Partially mitigated |
| Missing RBAC | Governance | High | Medium | Documented as production gap, planned for future governance sprint | Open |
| Missing formal migrations | Operations | Medium | Medium | SQLAlchemy create-all for MVP, Alembic planned | Open |
| Insufficient audit retention policy | Compliance | Medium | Medium | Audit data exists, retention policy documented as future control | Open |

## Highest Priority Risks

1. RBAC and access control for restricted data
2. Hallucination and unsupported financial claims
3. Prompt injection and data exfiltration attempts
4. SEC/FRED external API reliability
5. Cost and latency growth as data volume increases

## Risk Review Cadence

For a production pilot, this register should be reviewed:

- Before each release
- After model or embedding provider changes
- After adding new data sources
- After evaluation pass rate drops
- After any security or compliance incident
