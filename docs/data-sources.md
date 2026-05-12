# Data Sources

## SEC EDGAR APIs

Source: https://www.sec.gov/search-filings/edgar-application-programming-interfaces

用途：

- 公司 filings
- 10-K / 10-Q
- Company facts
- XBRL structured financial data

注意：

- SEC 要求合理的 request rate。
- `SEC_USER_AGENT` 應填入可識別的姓名與 email。
- 原始資料放入 `data/raw/`，處理後資料放入 `data/processed/`。

## FRED API

Source: https://fred.stlouisfed.org/docs/api/fred/

用途：

- Interest rates
- CPI
- GDP
- Unemployment rate
- Yield curve and other macro series

注意：

- 需要 `FRED_API_KEY`。
- 可先用 cached sample data 開發，再接 live API。

## Internal Policy Documents

Source: self-authored sample documents in `data/policies/`

用途：

- AI usage policy
- Data privacy policy
- Model risk policy
- Investment research review policy

這些文件用於展示 enterprise RAG、compliance QA、policy-grounded answer 與 AI governance 能力。
