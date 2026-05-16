# Security And Governance

## Current Controls

## Security Preflight

All chat requests pass through deterministic security preflight before agent routing.

Current actions:

- `allow`: continue normal workflow
- `mask`: replace sensitive values before routing
- `block`: return a `security-governance-agent` response without using downstream tools

Detected categories:

- Email
- Phone number
- SSN-like identifiers
- Payment card-like numbers
- Secret or API key-like tokens
- Prompt injection patterns
- Policy bypass attempts
- Hidden prompt extraction attempts

## Privacy And Audit Logging

Security audit records store:

- message hash
- role
- risk level
- action
- finding count
- agent
- timestamp

They do not store raw sensitive text.

## Policy RAG

The system includes enterprise-style internal policies:

- AI Usage Policy
- Data Privacy Policy
- Model Risk Management Policy
- Investment Research Review Policy
- Client Communication Policy

Policy answers are grounded in indexed policy documents and include citations.

## SQL Safety

The SQL Analytics Agent does not accept raw SQL and does not use LLM-generated SQL. It uses predefined metric templates for structured financial analytics.

## Evaluation Controls

The evaluation engine includes governance checks:

- `security-smoke`
- prompt injection block behavior
- PII masking behavior
- forbidden answer terms
- route accuracy
- citation and source checks

## Future Controls

## RBAC

Add role-aware policies for:

- research analyst
- compliance reviewer
- operations analyst
- admin
- read-only demo user

## SSO

Integrate enterprise identity through SSO before production use.

## Approval Workflow

Require human approval before:

- client-facing research output
- investment recommendations
- sensitive compliance decisions
- large batch ingestion runs

## Retention Policy

Define retention for:

- request logs
- security audit records
- evaluation reports
- indexed filing chunks
- raw SEC files

## Model Risk Review

For production, maintain:

- model inventory
- evaluation evidence
- known limitations
- approval checkpoints
- monitoring plan

## Enterprise Governance Fit

The current design demonstrates important financial enterprise expectations:

- source traceability
- no-answer behavior
- auditability
- deterministic evaluation
- prompt injection control
- privacy-aware logging
- safe structured analytics
