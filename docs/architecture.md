# Aurelia Ledger Architecture

## 系統目標

Aurelia Ledger 是企業級金融智能代理平台。它將文件檢索、宏觀資料、SQL analytics、政策合規與多代理 orchestration 結合，形成可追蹤、可評估、可監控的 AI workflow。

## 高層架構

```text
React Frontend
  |
FastAPI Gateway
  |
Settings / Auth / Request Logging
  |
LangGraph Orchestrator
  |
  |-- Document Research Agent -> Qdrant -> SEC filings / policy docs
  |-- Macro Analysis Agent -> FRED API / cached macro tables
  |-- SQL Analytics Agent -> PostgreSQL
  |-- Policy Compliance Agent -> Qdrant -> internal policies
  |-- Evaluation Runner -> eval suites / scoring reports
  |
Observability
  |-- traces
  |-- token usage
  |-- latency
  |-- estimated cost
  |-- quality metrics
```

## Agent Flow

1. 使用者在 frontend 提問。
2. FastAPI 接收 request 並建立 request id。
3. Orchestrator 判斷問題類型。
4. 對應 agent 執行資料檢索或工具調用。
5. Response composer 生成有引用來源的答案。
6. Metrics logger 記錄 latency、token、cost、source、agent trace。

## Data Flow

- SEC filings 進入 raw data，經 parser、chunker、embedding pipeline 後寫入 Qdrant。
- FRED macro series 經 connector 拉取後可寫入 PostgreSQL 或 local cache。
- Internal policies 以 markdown/pdf 形式保存，經 chunking 後進入 vector database。
- Evaluation dataset 以固定問題集測試 retrieval recall、faithfulness、latency 與 cost。

## Security and Governance

後續 phase 加入：

- PII masking
- Prompt injection detection
- Role-based access control
- Audit logs
- Model fallback policy
- Data retention policy
- Human approval step for sensitive workflows
