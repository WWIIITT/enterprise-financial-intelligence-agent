# Environment Variables

| Variable | Purpose |
| --- | --- |
| `LLM_API_KEY` | API key for the OpenAI-compatible chat provider |
| `LLM_BASE_URL` | Chat provider base URL, usually ending in `/v1` |
| `LLM_MODEL` | Chat model identifier |
| `EMBEDDING_API_KEY` | Optional separate key for embedding provider |
| `EMBEDDING_BASE_URL` | Optional separate embedding provider base URL |
| `EMBEDDING_MODEL` | Text embedding model used for Qdrant vectors |
| `DATABASE_URL` | PostgreSQL connection string |
| `QDRANT_URL` | Qdrant vector database URL |
| `REDIS_URL` | Redis connection string |
| `FRED_API_KEY` | Optional key for live FRED macro data |
| `SEC_USER_AGENT` | Required identifiable user agent for live SEC requests |

## Notes

- Do not commit `.env`
- Qdrant requires a text embedding model, not a reranker
- FRED has sample fallback for local demo
- SEC live ingestion should always use a real user agent
