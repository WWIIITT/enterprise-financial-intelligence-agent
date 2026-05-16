# Evaluation Report

## Summary

- Suite: `all`
- Pass rate: 0.8571
- Route accuracy: 0.9
- Citation score: 0.9444
- Source coverage: 1.0
- Average latency: 493.57 ms
- P95 latency: 1001 ms
- Hallucination risk count: 0

## Failed Cases

| Case | Agent | Failures |
| --- | --- | --- |
| sec_aapl_risk_factors | document-research-agent | citation missing term 10-K |
| sec_unsupported_claim | document-research-agent | expected agent rag-orchestrator-low-confidence, got document-research-agent; answer missing term not contain enough relevant evidence |

## Recommendations

- Review deterministic router terms for missed intents.
- Improve citation construction or expected citation terms.
- Triage failed cases before expanding the suite.
