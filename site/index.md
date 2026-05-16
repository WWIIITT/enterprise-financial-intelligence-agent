---
layout: home

hero:
  name: "Aurelia Ledger"
  text: "Enterprise Financial Intelligence Agent Platform"
  tagline: "A sprint-by-sprint learning site for a production-style AI agent portfolio project"
  actions:
    - theme: brand
      text: Start the Sprint Guide
      link: /sprints/sprint-01-rag-mvp
    - theme: alt
      text: Explore Concepts
      link: /concepts/rag-and-citations

features:
  - title: Senior AI Engineering
    details: RAG, Qdrant retrieval, SEC ingestion, macro data, SQL analytics, deterministic evaluation, and reliable FastAPI interfaces.
  - title: AI Solution Architecture
    details: Governance, risk controls, cost planning, deployment roadmap, observability, and business-value framing.
  - title: Interview-Ready Narrative
    details: Each sprint explains the goal, design decisions, workflow, validation, and how to discuss the work in an interview.
---

## What This Site Explains

Aurelia Ledger simulates an internal financial intelligence platform for research analysts, compliance reviewers, and operations teams. It combines document RAG, live SEC EDGAR ingestion, FRED macro data, structured SEC Company Facts, LangGraph routing, deterministic evaluation, security guardrails, and observability.

This site explains the project as a learning journey. It is not a discussion forum and it is not a replacement for the running dashboard. It is a public-facing knowledge base that explains how the system was built and why each engineering decision exists.

## Suggested Learning Path

1. Read the sprint guide from Sprint 1 to Sprint 10 to understand the project evolution.
2. Use the concept guide to study each technical building block in isolation.
3. Use the workflow guide to understand request lifecycles and data movement.
4. Use the reference section for APIs, environment variables, local run commands, and glossary terms.

## Current Platform Capabilities

| Area | Capability |
| --- | --- |
| Document intelligence | Policy and SEC filing RAG with citation-aware answers |
| Macro analysis | FRED or sample macro series summaries with cached observations |
| SQL analytics | Safe structured financial metric queries over PostgreSQL |
| Orchestration | LangGraph workflow with deterministic routing and multi-agent traces |
| Security | PII masking, prompt injection blocking, and audit records |
| Evaluation | Deterministic smoke suites, scoring, markdown and JSON reports |
| Observability | Request, evaluation, and security audit summaries in a custom dashboard |

## Portfolio Positioning

The project is designed to show both execution depth and architecture judgment:

- It starts with a narrow RAG MVP rather than a broad unfinished agent system.
- It adds real retrieval persistence before orchestration.
- It keeps SQL analytics deterministic and safe.
- It evaluates behavior with repeatable tests rather than vague demo claims.
- It surfaces security, cost, monitoring, and deployment concerns as first-class deliverables.
