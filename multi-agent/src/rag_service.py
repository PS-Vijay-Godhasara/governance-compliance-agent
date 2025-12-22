"""Multi-Agent RAG Service with Database Support"""

import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

class MultiAgentRAGService:
    def __init__(self, use_database: bool = True, db_path: str = "./chroma_db"):
        self.use_database = use_database and CHROMADB_AVAILABLE
        self.db_path = db_path
        self.client = None
        self.collection = None
        self.knowledge_cache = {}
        
        if self.use_database:
            self._init_database()
        else:
            self._init_file_based()
    
    def _init_database(self):
        """Initialize ChromaDB vector database"""
        try:
            self.client = chromadb.PersistentClient(
                path=self.db_path,
                settings=Settings(anonymized_telemetry=False)
            )
            self.collection = self.client.get_or_create_collection(
                name="governance_knowledge",
                metadata={"description": "Governance and compliance knowledge base"}
            )
        except Exception as e:
            print(f"Database initialization failed: {e}")
            self.use_database = False
            self._init_file_based()
    
    def _init_file_based(self):
        """Initialize file-based knowledge storage"""
        self.knowledge_cache = {
            "regulations": {
                "gdpr": "EU data protection regulation with strict consent requirements",
                "kyc": "Know Your Customer requirements for identity verification",
                "aml": "Anti-Money Laundering compliance for financial transactions"
            },
            "policies": {
                "customer_onboarding": "Customer registration validation requirements",
                "risk_assessment": "Transaction risk evaluation criteria"
            }
        }
    
    async def add_knowledge(self, document_id: str, content: str, metadata: Dict[str, Any] = None):
        """Add knowledge to the database"""
        if self.use_database:
            try:
                self.collection.add(
                    documents=[content],
                    ids=[document_id],
                    metadatas=[metadata or {}]
                )
            except Exception as e:
                print(f"Database add failed: {e}")
        else:
            # File-based fallback
            topic = metadata.get("topic", "general") if metadata else "general"
            if topic not in self.knowledge_cache:
                self.knowledge_cache[topic] = {}
            self.knowledge_cache[topic][document_id] = content
    
    async def search(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search knowledge base"""
        if self.use_database:
            return await self._vector_search(query, n_results)
        else:
            return await self._text_search(query, n_results)
    
    async def _vector_search(self, query: str, n_results: int) -> List[Dict[str, Any]]:
        """Vector-based semantic search"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            search_results = []
            if results["documents"]:
                for i, doc in enumerate(results["documents"][0]):
                    search_results.append({
                        "id": results["ids"][0][i],
                        "content": doc,
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                        "distance": results["distances"][0][i] if results["distances"] else 0.0,
                        "relevance": 1.0 - (results["distances"][0][i] if results["distances"] else 0.0)
                    })
            
            return search_results
        
        except Exception as e:
            print(f"Vector search failed: {e}")
            return await self._text_search(query, n_results)
    
    async def _text_search(self, query: str, n_results: int) -> List[Dict[str, Any]]:
        """Simple text-based search fallback"""
        results = []
        query_lower = query.lower()
        
        for topic, documents in self.knowledge_cache.items():
            for doc_id, content in documents.items():
                if query_lower in content.lower():
                    relevance = content.lower().count(query_lower) / len(content.split())
                    results.append({
                        "id": doc_id,
                        "content": content,
                        "metadata": {"topic": topic},
                        "relevance": min(relevance, 1.0)
                    })
        
        # Sort by relevance and return top results
        results.sort(key=lambda x: x["relevance"], reverse=True)
        return results[:n_results]
    
    async def get_context(self, policy_id: str, query: str = None) -> Dict[str, Any]:
        """Get contextual information for policy validation"""
        search_query = query or policy_id
        results = await self.search(search_query, 3)
        
        return {
            "policy_id": policy_id,
            "context_query": search_query,
            "related_knowledge": results,
            "timestamp": datetime.now().isoformat()
        }
    
    async def enhance_validation(self, policy_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance validation with contextual knowledge"""
        # Search for relevant compliance information
        context = await self.get_context(policy_id)
        
        # Extract relevant compliance requirements
        compliance_info = []
        for item in context["related_knowledge"]:
            if "compliance" in item["content"].lower() or "requirement" in item["content"].lower():
                compliance_info.append(item["content"])
        
        return {
            "enhanced_context": context,
            "compliance_requirements": compliance_info,
            "recommendations": self._generate_recommendations(policy_id, data, compliance_info)
        }
    
    def _generate_recommendations(self, policy_id: str, data: Dict[str, Any], compliance_info: List[str]) -> List[str]:
        """Generate validation recommendations"""
        recommendations = []
        
        # Basic recommendations based on policy type
        if "kyc" in policy_id.lower():
            recommendations.append("Ensure all identity documents are current and valid")
            recommendations.append("Verify customer against sanctions lists")
        
        if "customer" in policy_id.lower():
            recommendations.append("Validate email format and deliverability")
            recommendations.append("Check age requirements for jurisdiction")
        
        # Add compliance-specific recommendations
        for info in compliance_info:
            if "gdpr" in info.lower():
                recommendations.append("Ensure GDPR consent is properly documented")
            if "aml" in info.lower():
                recommendations.append("Perform AML screening for high-risk indicators")
        
        return recommendations
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Get knowledge base statistics"""
        if self.use_database:
            try:
                count = self.collection.count()
                return {
                    "total_documents": count,
                    "storage_type": "vector_database",
                    "database_path": self.db_path
                }
            except:
                pass
        
        # File-based statistics
        total_docs = sum(len(docs) for docs in self.knowledge_cache.values())
        return {
            "total_documents": total_docs,
            "storage_type": "file_based",
            "topics": list(self.knowledge_cache.keys())
        }