# Data Privacy and PII Handling Policy

## Policy Owner

Chief Privacy Office and Information Security.

## Purpose

This policy defines how personal data and confidential information must be handled when using AI systems, analytics platforms, document ingestion pipelines, and retrieval-augmented generation workflows.

## Data Classification

The firm classifies data into four levels:

- Public: information approved for public release, such as published SEC filings and public macroeconomic data.
- Internal: non-public business information intended for employee use.
- Confidential: sensitive business, client, vendor, or employee information.
- Restricted: regulated personal data, credentials, material non-public information, private keys, and highly sensitive legal or compliance records.

Restricted data must not be sent to unapproved AI services.

## PII Handling Rules

AI systems must mask or remove personal identifiers before model calls unless the use case has explicit privacy approval. Personal identifiers include names, addresses, phone numbers, email addresses, government IDs, account numbers, employee IDs, device identifiers, and any combination of attributes that can identify a person.

When PII is required for an approved workflow, the system must use the minimum necessary fields, apply role-based access control, and record an audit log.

## Document Ingestion Controls

Before documents are ingested into a vector database, the ingestion pipeline must determine the document classification. Public documents such as SEC filings may be indexed for research use. Confidential or Restricted documents require approval, access controls, retention rules, and deletion procedures before indexing.

## Retention and Deletion

Request logs, embeddings, retrieved chunks, and generated answers must follow retention schedules approved by Legal, Compliance, and Information Security. If a source document must be deleted, derived embeddings and cached chunks must also be deleted or rendered inaccessible.

## Third-Party AI Providers

Third-party AI providers must be reviewed for data processing terms, retention settings, regional processing, security certifications, and incident notification requirements. Teams must not use personal accounts or unmanaged API keys for firm data.

## Incident Escalation

Users must report suspected privacy incidents immediately when:

- PII is uploaded to an unapproved AI tool.
- Restricted data appears in model output.
- A prompt injection attempts to extract confidential data.
- Logs or vector stores expose data to unauthorized users.

The incident response team must assess impact, containment, notification obligations, and remediation steps.
