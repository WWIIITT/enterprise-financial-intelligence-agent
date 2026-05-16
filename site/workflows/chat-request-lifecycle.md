# Chat Request Lifecycle

## Purpose

This workflow explains what happens when a user sends a message to `/api/chat`.

## Flow

```mermaid
sequenceDiagram
    participant User
    participant API as FastAPI
    participant Security as Security Preflight
    participant Graph as LangGraph Orchestrator
    participant Agent as Selected Agent
    participant Logs as Request Logs

    User->>API: POST /api/chat
    API->>Security: check message
    alt blocked
        Security-->>API: block
        API-->>User: governance response
    else allow or mask
        Security-->>Graph: safe message
        Graph->>Graph: route decision
        Graph->>Agent: execute route
        Agent-->>Graph: answer, sources, trace, metrics
        Graph-->>API: ChatResponse
        API->>Logs: write request log
        API-->>User: answer + sources + trace
    end
```

## Key Decisions

- Security runs before retrieval or tool access.
- The frontend response shape stays stable.
- The trace exposes route decisions and agent execution.

## What To Watch In A Demo

Use the Agent Trace panel to show `security_preflight`, `route`, selected agent step, and `respond`.
