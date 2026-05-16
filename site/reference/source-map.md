# Source Map

This page maps learning topics to implementation files and GitHub line ranges.

Repository:

```text
https://github.com/WWIIITT/enterprise-financial-intelligence-agent
```

## RAG And Citations

| Area | Source |
| --- | --- |
| RAG response entrypoint | [rag_service.py L16-L84](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/rag_service.py#L16-L84) |
| Retrieval and reranking | [rag_service.py L132-L186](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/rag_service.py#L132-L186) |
| Evidence threshold | [rag_service.py L187-L228](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/rag_service.py#L187-L228) |
| Answer synthesis | [rag_service.py L238-L320](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/rag_service.py#L238-L320) |
| Chunking | [chunking.py L5-L24](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/rag/chunking.py#L5-L24) |

## Qdrant Vector Retrieval

| Area | Source |
| --- | --- |
| Qdrant store | [vector_store.py L18-L145](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/rag/vector_store.py#L18-L145) |
| Collection validation | [vector_store.py L157-L185](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/rag/vector_store.py#L157-L185) |
| Embedding client | [embedding_client.py L16-L84](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/rag/embedding_client.py#L16-L84) |
| Local fallback store | [store.py L11-L86](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/rag/store.py#L11-L86) |

## SEC EDGAR Ingestion

| Area | Source |
| --- | --- |
| SEC fetch entrypoint | [sec_edgar_client.py L23-L102](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/sec_edgar_client.py#L23-L102) |
| Filing cleaner and parser | [sec_edgar_client.py L103-L159](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/sec_edgar_client.py#L103-L159) |
| Filing selection | [sec_edgar_client.py L160-L223](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/sec_edgar_client.py#L160-L223) |
| Retry and throttling | [sec_edgar_client.py L231-L291](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/sec_edgar_client.py#L231-L291) |
| Live ingestion | [ingestion_service.py L53-L124](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/ingestion_service.py#L53-L124) |

## Macro Analysis

| Area | Source |
| --- | --- |
| Series catalog and sample data | [macro_service.py L18-L61](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/macro_service.py#L18-L61) |
| FRED client | [macro_service.py L62-L123](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/macro_service.py#L62-L123) |
| Analysis entrypoints | [macro_service.py L124-L187](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/macro_service.py#L124-L187) |
| Intent detection | [macro_service.py L188-L223](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/macro_service.py#L188-L223) |
| Cache and trend helpers | [macro_service.py L252-L392](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/macro_service.py#L252-L392) |

## SQL Analytics

| Area | Source |
| --- | --- |
| Metric whitelist | [sql_analytics_service.py L27-L67](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/sql_analytics_service.py#L27-L67) |
| Ingestion and analysis | [sql_analytics_service.py L95-L154](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/sql_analytics_service.py#L95-L154) |
| SEC facts parsing | [sql_analytics_service.py L155-L196](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/sql_analytics_service.py#L155-L196) |
| Persistence and queries | [sql_analytics_service.py L197-L260](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/sql_analytics_service.py#L197-L260) |
| Answer and route helpers | [sql_analytics_service.py L261-L349](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/sql_analytics_service.py#L261-L349) |

## LangGraph Orchestrator

| Area | Source |
| --- | --- |
| State and entrypoint | [orchestrator.py L19-L67](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/agents/orchestrator.py#L19-L67) |
| Route decision | [orchestrator.py L68-L82](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/agents/orchestrator.py#L68-L82) |
| Graph construction | [orchestrator.py L83-L120](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/agents/orchestrator.py#L83-L120) |
| Agent nodes | [orchestrator.py L121-L231](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/agents/orchestrator.py#L121-L231) |
| Response assembly | [orchestrator.py L232-L257](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/agents/orchestrator.py#L232-L257) |

## Evaluation Engine

| Area | Source |
| --- | --- |
| Entry points | [eval_service.py L27-L55](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/eval_service.py#L27-L55) |
| Case execution | [eval_service.py L56-L138](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/eval_service.py#L56-L138) |
| Scoring functions | [eval_service.py L139-L248](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/eval_service.py#L139-L248) |
| Metric aggregation | [eval_service.py L249-L283](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/eval_service.py#L249-L283) |
| Report writing | [eval_service.py L284-L344](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/eval_service.py#L284-L344) |

## Security Governance

| Area | Source |
| --- | --- |
| Detection patterns | [security_service.py L10-L27](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/security_service.py#L10-L27) |
| Security check | [security_service.py L28-L71](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/security_service.py#L28-L71) |
| Hashing and block answer | [security_service.py L72-L86](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/security_service.py#L72-L86) |
| PII and injection detection | [security_service.py L87-L127](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/security_service.py#L87-L127) |
| Action and risk mapping | [security_service.py L128-L147](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/security_service.py#L128-L147) |

## Observability Dashboard

| Area | Source |
| --- | --- |
| Summary aggregation | [observability_service.py L19-L81](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/observability_service.py#L19-L81) |
| Empty state | [observability_service.py L82-L97](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/observability_service.py#L82-L97) |
| Distribution and p95 | [observability_service.py L98-L128](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/services/observability_service.py#L98-L128) |
| Request log model | [models.py L38-L49](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/models.py#L38-L49) |
| Evaluation run model | [models.py L94-L104](https://github.com/WWIIITT/enterprise-financial-intelligence-agent/blob/main/backend/app/models.py#L94-L104) |
