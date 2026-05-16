# SQL Analytics Flow

## Purpose

This workflow explains how structured financial facts are ingested and queried safely.

## Flow

```mermaid
flowchart TD
    Ingest[Ingest Company Facts] --> SEC[SEC Company Facts API or Sample]
    SEC --> Normalize[Normalize Concepts]
    Normalize --> Facts[(PostgreSQL Financial Facts)]
    Analyze[SQL Analyze Request] --> Validate[Validate Metric]
    Validate --> Template[Safe Query Template]
    Template --> Facts
    Facts --> Response[Trend Summary + Sources]
```

## Safety Rule

The system does not accept raw SQL and does not ask an LLM to generate SQL. It only supports predefined metrics and query templates.

## What To Watch In A Demo

Run company facts ingestion for AAPL, then analyze annual revenue. The response should cite SEC Company Facts.
