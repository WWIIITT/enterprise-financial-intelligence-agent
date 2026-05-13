# AI Usage Policy

## Policy Owner

Enterprise AI Governance Committee.

## Purpose

This policy defines approved and prohibited uses of generative AI, AI agents, retrieval systems, and automated research assistants inside the firm. It applies to employees, contractors, consultants, and system accounts that use AI tools for investment research, operations, compliance, client service, and engineering.

## Approved Use Cases

Employees may use approved AI tools for:

- Summarizing public SEC filings, earnings transcripts, macroeconomic releases, and internal policy documents.
- Drafting internal research notes when the output is reviewed by an accountable employee.
- Generating SQL drafts against approved analytics schemas, subject to query review and access controls.
- Classifying support tickets, operational incidents, and internal knowledge-base articles.
- Producing code suggestions for non-production changes, provided normal code review and security checks remain in place.

AI output must be treated as an analytical aid, not as an authoritative record or final investment recommendation.

## Prohibited Use Cases

Employees must not use AI systems to:

- Upload client confidential information, material non-public information, credentials, private keys, or regulated personal data into unapproved tools.
- Generate client-facing investment recommendations without human review and documented approval.
- Bypass research supervision, compliance review, model risk review, or data access controls.
- Ask a model to hide, remove, or ignore audit trails.
- Execute trades, approve transactions, or make employment, credit, insurance, or legal decisions without approved workflow controls.

## Human Review Requirements

All AI-generated research summaries must be reviewed by a qualified employee before distribution. The reviewer must verify source citations, check numerical claims, confirm that assumptions are reasonable, and record any material edits. For high-impact investment research, review evidence must be retained with the research package.

## Source Citation Requirements

AI answers that rely on external or internal documents must include citations. A valid citation should identify the source document, section or chunk, and retrieval context when available. If the system cannot find supporting evidence, it must say that evidence is unavailable rather than inventing a source.

## Escalation

Users must escalate to Compliance or the AI Governance Committee when:

- The request involves client data, employee data, or sensitive business information.
- The answer may influence investment decisions, trading activity, or external communications.
- The model appears to hallucinate, cite irrelevant documents, or ignore policy instructions.
- A prompt injection attempt is detected in retrieved content or user input.

## Audit and Monitoring

Approved AI applications must log request timestamp, user or service identity, selected agent route, model name, data sources used, latency, estimated cost, and error status. Logs must be retained according to the firm's technology and compliance retention schedules.
