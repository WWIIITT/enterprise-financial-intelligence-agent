# Qdrant Vector Retrieval

## Definition

Qdrant is the vector database used to store embedded document chunks and retrieve semantically similar chunks for a query.

## Why It Exists In Aurelia Ledger

The platform needs persistent retrieval across backend restarts. Qdrant gives the project a realistic production-style retrieval layer instead of relying on in-memory development search.

## How It Works In This Repo

- Policy and SEC chunks are embedded with provider embeddings.
- The Qdrant collection is created based on the first embedding dimension.
- Query embeddings search the collection.
- Payload metadata stores title, source type, citation, URL, section, and chunk text.

## Design Tradeoffs

- Provider embeddings improve retrieval quality but require configuration.
- Collection dimension validation prevents silent model mismatch.
- In-memory fallback remains useful for tests but is not the primary production path.

## Failure Modes

- Embedding model is missing.
- Provider does not support embeddings.
- Existing Qdrant collection has a different vector dimension.
- Bad chunking causes relevant evidence to rank poorly.

## Interview Explanation

Qdrant is used because the platform needs durable vector search with metadata payloads and predictable retrieval behavior.
