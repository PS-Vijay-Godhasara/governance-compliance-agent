"""Simple RAG Service - File-based knowledge retrieval"""

import json
import os
from typing import Dict, List, Any, Optional

class SimpleRAGService:
    def __init__(self, knowledge_dir: str = "./knowledge"):
        self.knowledge_dir = knowledge_dir
        self.knowledge_base = {}
        self._load_knowledge()
    
    def _load_knowledge(self):
        """Load knowledge from JSON files"""
        if not os.path.exists(self.knowledge_dir):
            os.makedirs(self.knowledge_dir)
            self._create_sample_knowledge()
        
        for filename in os.listdir(self.knowledge_dir):
            if filename.endswith('.json'):
                topic = filename[:-5]
                with open(os.path.join(self.knowledge_dir, filename), 'r') as f:
                    self.knowledge_base[topic] = json.load(f)
    
    def _create_sample_knowledge(self):
        """Create sample knowledge files"""
        knowledge = {
            "regulations": {
                "gdpr": {
                    "description": "EU General Data Protection Regulation",
                    "key_requirements": ["consent", "data_minimization", "right_to_erasure"],
                    "penalties": "Up to 4% of annual revenue"
                },
                "kyc": {
                    "description": "Know Your Customer requirements",
                    "documents_required": ["government_id", "proof_of_address"],
                    "risk_categories": ["low", "medium", "high"]
                }
            },
            "policies": {
                "customer_onboarding": {
                    "purpose": "Validate new customer registration",
                    "required_fields": ["email", "age", "phone"],
                    "business_rules": ["age >= 18", "valid email format"]
                }
            }
        }
        
        for topic, data in knowledge.items():
            with open(os.path.join(self.knowledge_dir, f"{topic}.json"), 'w') as f:
                json.dump(data, f, indent=2)
    
    def search(self, query: str, topic: Optional[str] = None) -> List[Dict[str, Any]]:
        """Simple text-based search"""
        results = []
        query_lower = query.lower()
        
        search_topics = [topic] if topic else self.knowledge_base.keys()
        
        for search_topic in search_topics:
            if search_topic not in self.knowledge_base:
                continue
                
            data = self.knowledge_base[search_topic]
            matches = self._search_in_data(data, query_lower, search_topic)
            results.extend(matches)
        
        return results[:5]  # Return top 5 matches
    
    def _search_in_data(self, data: Any, query: str, topic: str, path: str = "") -> List[Dict[str, Any]]:
        """Recursively search in data structure"""
        matches = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{path}.{key}" if path else key
                
                # Check if query matches key or string values
                if query in key.lower():
                    matches.append({
                        "topic": topic,
                        "path": current_path,
                        "content": value,
                        "relevance": 0.8
                    })
                
                if isinstance(value, str) and query in value.lower():
                    matches.append({
                        "topic": topic,
                        "path": current_path,
                        "content": value,
                        "relevance": 0.6
                    })
                
                # Recurse into nested structures
                matches.extend(self._search_in_data(value, query, topic, current_path))
        
        elif isinstance(data, list):
            for i, item in enumerate(data):
                current_path = f"{path}[{i}]" if path else f"[{i}]"
                matches.extend(self._search_in_data(item, query, topic, current_path))
        
        return matches
    
    def get_context(self, policy_id: str) -> Dict[str, Any]:
        """Get contextual information for a policy"""
        context = {"policy_id": policy_id, "related_info": []}
        
        # Search for related information
        results = self.search(policy_id)
        context["related_info"] = results
        
        return context
    
    def add_knowledge(self, topic: str, data: Dict[str, Any]):
        """Add knowledge to the base"""
        self.knowledge_base[topic] = data
        
        # Save to file
        with open(os.path.join(self.knowledge_dir, f"{topic}.json"), 'w') as f:
            json.dump(data, f, indent=2)
    
    def list_topics(self) -> List[str]:
        """List available knowledge topics"""
        return list(self.knowledge_base.keys())