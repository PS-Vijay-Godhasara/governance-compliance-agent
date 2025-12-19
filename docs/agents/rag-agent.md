# RAG Agent Documentation

## Overview
The RAG Agent provides knowledge retrieval and context management using vector databases.

## Core Actions

### `store_knowledge`
**Input:**
```json
{
  "content": "GDPR requires explicit consent for data processing",
  "type": "regulation",
  "id": "gdpr_consent",
  "metadata": {"jurisdiction": "EU", "regulation": "GDPR"}
}
```

**Output:**
```json
{
  "doc_id": "gdpr_consent",
  "stored": true
}
```

### `retrieve_context`
**Input:**
```json
{
  "query": "customer age requirements",
  "type": "policy",
  "limit": 5
}
```

**Output:**
```json
{
  "context": [
    {
      "content": "All customers must be 18 or older...",
      "metadata": {"policy_id": "age_policy"},
      "score": 0.95
    }
  ]
}
```

### `semantic_search`
Performs semantic search across knowledge base with similarity threshold.

## Usage Example

```python
from src.agents.rag_agent import RAGAgent

rag_agent = RAGAgent()
await rag_agent.initialize()

# Store knowledge
store_message = AgentMessage(
    sender="user",
    recipient="rag",
    action="store_knowledge",
    payload={
        "content": "All transactions over $10,000 require approval",
        "type": "policy",
        "id": "transaction_limit"
    }
)

# Search knowledge
search_message = AgentMessage(
    sender="user",
    recipient="rag",
    action="retrieve_context",
    payload={
        "query": "transaction approval limits",
        "limit": 3
    }
)

response = await rag_agent.process_message(search_message)
```

## Configuration
- Uses ChromaDB for vector storage
- Sentence transformers for embeddings
- Fallback to keyword search if vector DB unavailable