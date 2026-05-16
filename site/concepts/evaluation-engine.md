# Evaluation Engine

## Definition

The Evaluation Engine runs deterministic test cases against chat and endpoint behavior, then scores route accuracy, source coverage, citations, answer terms, latency, and hallucination-risk flags.

## Why It Exists In Aurelia Ledger

Enterprise AI needs quality tracking. Manual demos are not enough to show reliability.

## How It Works In This Repo

- JSON fixtures define expected agents, sources, citations, and answer terms.
- `/api/evals/run` executes a suite.
- `/api/evals/report` writes markdown and JSON reports.
- Evaluation run records are stored in PostgreSQL.

## Design Tradeoffs

- Deterministic checks are repeatable and low cost.
- They are a proxy for semantic quality, not a full human review.
- LLM-as-judge can be added later when cost and variance are acceptable.

## Failure Modes

- Tests can become too brittle.
- Required terms may miss valid paraphrases.
- Passing smoke tests does not guarantee full production quality.

## Interview Explanation

The evaluation system shows that each agent route is measurable. It gives concrete quality evidence instead of relying on subjective demos.
