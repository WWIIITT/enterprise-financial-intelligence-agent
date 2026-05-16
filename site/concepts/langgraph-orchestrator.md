# LangGraph Orchestrator

## Definition

The LangGraph Orchestrator is the workflow layer behind `/api/chat`. It decides which agent path should handle a question and assembles traceable response steps.

## Why It Exists In Aurelia Ledger

The platform has multiple agents and tools. Routing logic must be explicit, testable, and visible in traces.

## How It Works In This Repo

- Security preflight runs before the graph.
- Deterministic router selects policy, document, macro, macro-document, SQL, or fallback.
- Agent nodes call existing services.
- Response shape remains stable for the frontend.

## Design Tradeoffs

- Deterministic routing is cheaper and easier to evaluate than LLM routing.
- Rule-based routing can miss unusual phrasing.
- Keeping the public API stable protects the frontend from backend refactors.

## Failure Modes

- Ambiguous questions may route to the wrong agent.
- Multi-agent synthesis can become too broad.
- Routing rules must evolve with new agent capabilities.

## Interview Explanation

LangGraph is used for workflow clarity, not for hype. It makes route decisions and trace steps explicit.
