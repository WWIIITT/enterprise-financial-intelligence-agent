# Model Risk Management Policy

## Policy Owner

Model Risk Management and Enterprise AI Governance Committee.

## Purpose

This policy defines governance expectations for AI models, AI agents, retrieval pipelines, prompt templates, evaluation datasets, and automated decision-support workflows used by the firm.

## Model Inventory

Every production AI system must be registered in the model inventory. The inventory must record model provider, model version, use case owner, data sources, deployment environment, approval status, limitations, monitoring metrics, and fallback procedures.

## Risk Tiering

AI systems must be assigned a risk tier:

- Low risk: internal productivity use with no client, trading, compliance, or regulated decision impact.
- Medium risk: internal research, operational workflow support, or policy QA with human review.
- High risk: workflows that may influence investment decisions, external communications, regulated reporting, trading, credit, employment, or client outcomes.

High-risk systems require formal validation before production release.

## Validation Requirements

Validation must include:

- Retrieval quality testing for RAG systems.
- Faithfulness and hallucination evaluation.
- Citation correctness checks.
- Prompt injection and data leakage testing.
- Latency, reliability, and cost testing.
- Human review of representative outputs.

Evaluation evidence must be stored with the model approval record.

## Change Management

Material changes require review. Material changes include switching model provider, changing model version, changing embedding model, modifying routing logic, adding new data sources, changing prompts that affect output behavior, or expanding the user population.

## Monitoring

Production AI systems must monitor:

- Error rate.
- Latency.
- Token usage and estimated cost.
- Retrieval score and source coverage.
- Route selection.
- User feedback.
- Policy violations.
- Hallucination or unsupported-answer reports.

Metrics must be reviewed by the system owner and escalated when thresholds are breached.

## Limitations Disclosure

AI systems must disclose relevant limitations. The system must not claim certainty when evidence is incomplete. For financial analysis, generated content must not be represented as final investment advice without human review and approval.
