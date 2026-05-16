# RAG And Citations

## Definition

Retrieval-Augmented Generation, or RAG, answers a question by retrieving relevant source text before composing a response. In Aurelia Ledger, RAG is citation-aware: answers must expose the source chunks used as evidence.

## Why It Exists In Aurelia Ledger

Financial and compliance answers need evidence. A useful answer is not only fluent; it must point back to SEC filings or internal policy documents.

## How It Works In This Repo

1. Documents are cleaned and chunked.
2. Chunks are embedded and indexed in Qdrant.
3. User questions are embedded.
4. Qdrant retrieves candidate chunks.
5. Lightweight reranking and confidence checks filter weak evidence.
6. The response includes answer text, source list, trace, and metrics.

## Design Tradeoffs

- Deterministic synthesis keeps cost low and reduces hallucination risk.
- Citation formatting is easier to evaluate than free-form long answers.
- Retrieval quality depends on chunking, embeddings, and reranking.

## Failure Modes

- Weak retrieval can surface unrelated policy chunks.
- Overly large chunks can dilute evidence.
- Overly small chunks can lose context.
- Missing citations reduce trust even when the answer is correct.

## Interview Explanation

The project treats citations as a product requirement, not a cosmetic detail. In finance, the user needs to know which document supports each claim.
