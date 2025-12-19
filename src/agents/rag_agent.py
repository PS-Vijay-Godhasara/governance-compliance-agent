"""RAG Agent for knowledge retrieval and context management"""

import asyncio
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent, AgentMessage, AgentResponse
import logging

logger = logging.getLogger(__name__)


class RAGAgent(BaseAgent):
    """Agent for Retrieval-Augmented Generation"""
    
    def __init__(self):
        super().__init__("RAGAgent")
        self.vector_db = None
        self.embeddings_model = None
        self.knowledge_base = {}
        
    async def initialize(self):
        """Initialize RAG components"""
        try:
            # Initialize ChromaDB (lightweight vector database)
            import chromadb
            from chromadb.config import Settings
            
            self.vector_db = chromadb.Client(Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory="./chroma_db"
            ))
            
            # Create collections
            self.policy_collection = self.vector_db.get_or_create_collection("policies")
            self.regulation_collection = self.vector_db.get_or_create_collection("regulations")
            
            # Initialize embeddings (using sentence-transformers)
            try:
                from sentence_transformers import SentenceTransformer
                self.embeddings_model = SentenceTransformer('all-MiniLM-L6-v2')
            except ImportError:
                logger.warning("sentence-transformers not available, using simple embeddings")
                self.embeddings_model = None
            
            logger.info("RAGAgent initialized with vector database")
            
        except Exception as e:
            logger.error(f"RAG initialization error: {e}")
            # Fallback to simple in-memory storage
            self.vector_db = None
            self.embeddings_model = None
    
    async def process_message(self, message: AgentMessage) -> AgentResponse:
        """Process RAG-related messages"""
        try:
            if message.action == "store_knowledge":
                return await self._store_knowledge(message.payload)
            elif message.action == "retrieve_context":
                return await self._retrieve_context(message.payload)
            elif message.action == "semantic_search":
                return await self._semantic_search(message.payload)
            else:
                return AgentResponse(success=False, error=f"Unknown action: {message.action}")
        except Exception as e:
            return AgentResponse(success=False, error=str(e))
    
    async def _store_knowledge(self, payload: Dict[str, Any]) -> AgentResponse:
        """Store knowledge in vector database"""
        try:
            content = payload.get("content", "")
            doc_type = payload.get("type", "policy")
            doc_id = payload.get("id", f"doc_{len(self.knowledge_base)}")
            metadata = payload.get("metadata", {})
            
            # Store in memory fallback
            self.knowledge_base[doc_id] = {
                "content": content,
                "type": doc_type,
                "metadata": metadata
            }
            
            # Store in vector DB if available
            if self.vector_db and self.embeddings_model:
                embedding = self.embeddings_model.encode([content])[0].tolist()
                
                collection = self.policy_collection if doc_type == "policy" else self.regulation_collection
                collection.add(
                    embeddings=[embedding],
                    documents=[content],
                    metadatas=[metadata],
                    ids=[doc_id]
                )
            
            return AgentResponse(
                success=True,
                data={"doc_id": doc_id, "stored": True}
            )
            
        except Exception as e:
            logger.error(f"Knowledge storage error: {e}")
            return AgentResponse(success=False, error=str(e))
    
    async def _retrieve_context(self, payload: Dict[str, Any]) -> AgentResponse:
        """Retrieve relevant context for a query"""
        try:
            query = payload.get("query", "")
            doc_type = payload.get("type", "policy")
            limit = payload.get("limit", 5)
            
            if self.vector_db and self.embeddings_model:
                # Semantic search using vector DB
                query_embedding = self.embeddings_model.encode([query])[0].tolist()
                
                collection = self.policy_collection if doc_type == "policy" else self.regulation_collection
                results = collection.query(
                    query_embeddings=[query_embedding],
                    n_results=limit
                )
                
                context = []
                for i, doc in enumerate(results['documents'][0]):
                    context.append({
                        "content": doc,
                        "metadata": results['metadatas'][0][i],
                        "score": results['distances'][0][i] if 'distances' in results else 1.0
                    })
                
            else:
                # Fallback: simple keyword matching
                context = []
                query_words = query.lower().split()
                
                for doc_id, doc_data in self.knowledge_base.items():
                    if doc_data["type"] == doc_type:
                        content_lower = doc_data["content"].lower()
                        score = sum(1 for word in query_words if word in content_lower)
                        
                        if score > 0:
                            context.append({
                                "content": doc_data["content"],
                                "metadata": doc_data["metadata"],
                                "score": score / len(query_words)
                            })
                
                # Sort by relevance score
                context.sort(key=lambda x: x["score"], reverse=True)
                context = context[:limit]
            
            return AgentResponse(
                success=True,
                data={"context": context, "query": query}
            )
            
        except Exception as e:
            logger.error(f"Context retrieval error: {e}")
            return AgentResponse(success=False, error=str(e))
    
    async def _semantic_search(self, payload: Dict[str, Any]) -> AgentResponse:
        """Perform semantic search across knowledge base"""
        try:
            query = payload.get("query", "")
            threshold = payload.get("threshold", 0.7)
            
            # Use retrieve_context for now
            context_response = await self._retrieve_context({
                "query": query,
                "type": "policy",
                "limit": 10
            })
            
            if context_response.success:
                # Filter by threshold
                filtered_results = [
                    item for item in context_response.data["context"]
                    if item["score"] >= threshold
                ]
                
                return AgentResponse(
                    success=True,
                    data={"results": filtered_results, "total": len(filtered_results)}
                )
            else:
                return context_response
                
        except Exception as e:
            logger.error(f"Semantic search error: {e}")
            return AgentResponse(success=False, error=str(e))