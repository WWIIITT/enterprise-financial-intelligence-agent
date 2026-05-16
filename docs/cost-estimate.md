# Cost Estimate

This document estimates cost drivers for Aurelia Ledger without relying on hard provider pricing. Provider prices change over time, so formulas and control levers are more useful than static numbers.

## Cost Drivers

| Component | Cost Driver | Notes |
| --- | --- | --- |
| LLM chat model | input tokens + output tokens | Current MVP keeps many responses deterministic to reduce cost |
| Embeddings | number of chunks embedded | SEC filings can create hundreds of chunks per filing |
| Qdrant | vector count + vector dimension + storage | Local Docker has no cloud cost, hosted Qdrant would scale with data volume |
| PostgreSQL | storage + compute | Stores metadata, financial facts, macro cache, logs, eval runs, security audits |
| SEC ingestion | network and processing time | SEC API itself is free but must be throttled and identified |
| FRED ingestion | API calls + cache storage | FRED is cached to reduce repeated API calls |
| Observability | log volume and retention | Request/security/eval logs grow with usage |

## Local Demo Cost

Typical local demo:

- Docker Compose for PostgreSQL, Qdrant, Redis
- Local frontend and backend
- Optional live SEC and FRED API calls
- Embedding API cost only when ingesting documents with provider embeddings
- Minimal or zero LLM cost if deterministic synthesis paths are used

Formula:

```text
demo_cost =
  embedding_chunks * embedding_cost_per_chunk
  + llm_input_tokens * input_token_rate
  + llm_output_tokens * output_token_rate
```

## Small Production Pilot Estimate

Assume:

- 5 to 20 internal users
- 10 to 50 chat requests per user per day
- 10 to 100 company filings indexed
- Daily or weekly macro refresh
- Evaluation suite run on demand or nightly

Main cost pressure will come from:

- Initial embedding of SEC filings
- Re-indexing when filing corpus changes
- Long analytical questions that trigger RAG + macro + SQL flows
- Retaining observability logs without pruning

## Cost Control Levers

- Cache macro data and company facts
- Reuse Qdrant indexes instead of re-embedding unchanged documents
- Limit top-k retrieval and reranking candidates
- Keep simple synthesis deterministic where possible
- Batch embeddings during ingestion
- Add retention policy for request and audit logs
- Use smaller embedding models for MVP workloads
- Use model fallback only for high-value requests

## Cost Monitoring Signals

- Total requests per day
- Average retrieved chunks per request
- Embedding chunks indexed per day
- Average latency and p95 latency
- Estimated cost per request
- Evaluation cost per run
- Storage growth in PostgreSQL and Qdrant

## Recommendation

For portfolio and pilot use, keep deterministic synthesis as the default and only introduce LLM-heavy answer generation after evaluation, cost tracking, and governance controls are stable.
