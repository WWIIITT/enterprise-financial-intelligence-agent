# Demo Script

Target length: 5 to 8 minutes

## 1. Opening

Talk track:

> Aurelia Ledger is an enterprise financial intelligence agent platform. It combines SEC filing RAG, FRED macro analysis, SEC Company Facts SQL analytics, policy compliance, LangGraph routing, deterministic evaluation, security guardrails, and observability.

## 2. Start Services

PowerShell:

```powershell
docker compose -f infra\docker-compose.yml up -d
cd backend
..\.venv\Scripts\python -m uvicorn app.main:app
```

In another terminal:

```powershell
cd frontend
npm run dev
```

## 3. Health And Config

```powershell
Invoke-RestMethod http://localhost:8000/health
Invoke-RestMethod http://localhost:8000/api/config/status
```

Browser talking point:

> The dashboard exposes backend readiness, configured services, and the agent console.

## 4. Ingest Policy Documents

```powershell
Invoke-RestMethod -Method Post http://localhost:8000/api/ingest/policy `
  -ContentType "application/json" `
  -Body '{"source":"all"}'
```

Talking point:

> These policies represent enterprise governance documents used by the Policy Compliance Agent.

## 5. Ingest Live SEC Filing

```powershell
Invoke-RestMethod -Method Post http://localhost:8000/api/ingest/sec `
  -ContentType "application/json" `
  -Body '{"source":"edgar","ticker":"AAPL","form_type":"10-K","filing_year":2025}'
```

Talking point:

> The system fetches an SEC filing, parses sections, chunks text, embeds chunks, and indexes them into Qdrant.

## 6. Ask Policy Question

```powershell
Invoke-RestMethod -Method Post http://localhost:8000/api/chat `
  -ContentType "application/json" `
  -Body '{"message":"What does the AI Usage Policy say about approved use?"}'
```

Talking point:

> The workflow routes to the Policy Compliance Agent and returns cited evidence.

## 7. Ask SEC Risk Question

```powershell
Invoke-RestMethod -Method Post http://localhost:8000/api/chat `
  -ContentType "application/json" `
  -Body '{"message":"What risks are mentioned for Apple?"}'
```

Talking point:

> This demonstrates source-grounded document research using SEC filing citations.

## 8. Macro Analysis

```powershell
Invoke-RestMethod -Method Post http://localhost:8000/api/macro/analyze `
  -ContentType "application/json" `
  -Body '{"series_ids":["FEDFUNDS","CPIAUCSL","UNRATE"],"question":"How do current rates and inflation affect Apple risk?"}'
```

Talking point:

> Macro data is fetched from FRED or cache, then summarized with deterministic trend checks.

## 9. SQL Analytics

```powershell
Invoke-RestMethod -Method Post http://localhost:8000/api/ingest/company-facts `
  -ContentType "application/json" `
  -Body '{"ticker":"AAPL","source":"sec-company-facts","use_sample_fallback":true}'
```

```powershell
Invoke-RestMethod -Method Post http://localhost:8000/api/sql/analyze `
  -ContentType "application/json" `
  -Body '{"ticker":"AAPL","metric":"revenue","period":"annual","limit":5}'
```

Talking point:

> SQL analytics is deterministic and safe. The system does not accept raw SQL from users.

## 10. Security Check

```powershell
Invoke-RestMethod -Method Post http://localhost:8000/api/security/check `
  -ContentType "application/json" `
  -Body '{"message":"Contact analyst at test@example.com about Apple risk","role":"research_analyst"}'
```

Talking point:

> Sensitive text is masked before routing, and prompt injection requests are blocked.

## 11. Evaluation Report

```powershell
Invoke-RestMethod -Method Post http://localhost:8000/api/evals/report `
  -ContentType "application/json" `
  -Body '{"suite":"all"}'
```

Talking point:

> Evaluation covers routing, source coverage, citation terms, answer terms, latency, hallucination-risk flags, security, and observability.

## 12. Observability Dashboard

```powershell
Invoke-RestMethod http://localhost:8000/api/observability/summary
```

Talking point:

> Observability uses request logs, evaluation runs, and security audits to show route distribution, latency, evaluation status, and governance events.

## 13. Close

Talking point:

> The value is not just one agent. The value is an enterprise pattern: grounded answers, tool routing, deterministic evaluation, governance controls, and operational visibility.
