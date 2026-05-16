# Security Preflight Flow

## Purpose

This workflow explains how the system handles sensitive or malicious input before agent routing.

## Flow

```mermaid
flowchart TD
    Message[User Message] --> Detect[PII and Injection Detection]
    Detect --> Risk[Risk Level]
    Risk -->|low| Allow[Allow]
    Risk -->|medium| Mask[Mask Sensitive Values]
    Risk -->|high| Block[Block Request]
    Allow --> Audit[(Audit Hash)]
    Mask --> Audit
    Block --> Audit
    Mask --> Orchestrator[Continue With Masked Message]
    Allow --> Orchestrator
    Block --> Response[Governance Response]
```

## Current Controls

- Email, phone, SSN, card-like, and secret-like token detection
- Prompt injection and policy bypass pattern detection
- Message hash audit records

## What To Watch In A Demo

Run a standalone security check with an email address, then run a prompt injection message through `/api/chat`.
