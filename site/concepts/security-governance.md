# Security Governance

## Definition

Security governance is the set of controls that detect sensitive input, block prompt injection, mask PII, and create audit records without storing raw sensitive text.

## Why It Exists In Aurelia Ledger

Financial enterprise systems must protect client data, confidential information, and policy boundaries before any agent or tool executes.

## How It Works In This Repo

- `/api/security/check` runs standalone guardrail checks.
- `/api/chat` runs security preflight before LangGraph routing.
- Medium-risk PII is masked.
- High-risk prompt injection is blocked.
- Security audit records store message hash, risk level, action, finding count, and agent.

## Design Tradeoffs

- Rule-based checks are transparent and fast.
- They do not replace complete enterprise DLP or access control.
- The MVP avoids storing raw sensitive text.

## Failure Modes

- Sophisticated prompt injection may bypass patterns.
- False positives can block legitimate requests.
- Future RBAC and SSO are still needed.

## Interview Explanation

The project puts security before retrieval and tool use. That ordering matters because unsafe input should not reach downstream agents.
