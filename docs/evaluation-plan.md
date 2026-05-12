# Evaluation Plan

## 評估目標

Aurelia Ledger 的 evaluation 不只測模型回答好不好，也要測 retrieval、agent routing、latency、cost、citation 與 governance behavior。

## 評估類型

### Retrieval Evaluation

- Top-k recall
- Citation correctness
- Source coverage
- No-answer behavior

### Answer Quality

- Faithfulness
- Completeness
- Financial reasoning clarity
- Hallucination rate

### Agent Workflow

- Router accuracy
- Tool selection correctness
- Multi-step trace completeness
- Failure fallback behavior

### Production Metrics

- Latency p50 / p95
- Token usage
- Estimated cost per request
- Error rate
- Timeout rate

### Governance Tests

- PII masking
- Prompt injection refusal
- Restricted data access behavior
- Audit log completeness

## Initial Eval Suites

- `smoke`: basic endpoint and response shape checks
- `rag_factual`: factual questions requiring cited answers
- `macro_analysis`: FRED-based macro reasoning
- `policy_compliance`: internal policy QA
- `multi_agent`: questions requiring more than one agent
