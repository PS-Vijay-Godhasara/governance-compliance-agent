"""Simple Orchestrator for Governance Workflows"""

from typing import Dict, Any, List
from engine import SimpleGovernanceEngine, ValidationResult
from rag_service import SimpleRAGService
from mcp_server import SimpleMCPServer

class SimpleOrchestrator:
    def __init__(self, use_llm: bool = False, policies_dir: str = "./policies"):
        self.engine = SimpleGovernanceEngine(policies_dir, use_llm)
        self.use_llm = use_llm
        self.rag_service = SimpleRAGService()
        self.mcp_server = SimpleMCPServer()
    
    def validate(self, policy_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data against policy"""
        result = self.engine.validate(policy_id, data)
        
        return {
            "is_valid": result.is_valid,
            "score": result.score,
            "violations": result.violations,
            "explanations": result.explanations,
            "summary": result.summary
        }
    
    def validate_kyc(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """KYC validation workflow"""
        result = self.engine.validate("kyc_validation", data)
        
        # Determine KYC status
        if result.score >= 0.8:
            status = "APPROVED"
            risk_level = "LOW"
        elif result.score >= 0.5:
            status = "REVIEW_REQUIRED"
            risk_level = "MEDIUM"
        else:
            status = "REJECTED"
            risk_level = "HIGH"
        
        return {
            "kyc_status": status,
            "risk_level": risk_level,
            "score": result.score,
            "violations": result.violations,
            "explanation": result.summary
        }
    
    def assess_risk(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Risk assessment workflow"""
        if self.use_llm and self.engine.llm_service:
            return self.engine.llm_service.assess_risk(data)
        
        # Simple rule-based risk assessment
        risk_score = 0.0
        risk_factors = []
        
        amount = data.get("amount", 0)
        if amount > 10000:
            risk_score += 0.4
            risk_factors.append("High transaction amount")
        
        if data.get("country") in ["XX", "YY"]:
            risk_score += 0.3
            risk_factors.append("High-risk country")
        
        if data.get("age", 25) < 21:
            risk_score += 0.2
            risk_factors.append("Young customer")
        
        risk_level = "HIGH" if risk_score >= 0.7 else "MEDIUM" if risk_score >= 0.3 else "LOW"
        
        return {
            "risk_level": risk_level,
            "risk_score": min(1.0, risk_score),
            "risk_factors": risk_factors,
            "requires_approval": risk_score >= 0.5,
            "explanation": f"Risk assessment: {risk_level} based on {len(risk_factors)} factors"
        }
    
    def create_policy(self, policy_text: str, policy_id: str) -> Dict[str, Any]:
        """Create policy from natural language"""
        return self.engine.create_policy_from_text(policy_text, policy_id)
    
    def list_policies(self) -> List[str]:
        """List available policies"""
        return self.engine.list_policies()
    
    def get_policy(self, policy_id: str) -> Dict[str, Any]:
        """Get policy details"""
        return self.engine.get_policy(policy_id)
    
    def search_knowledge(self, query: str, topic: str = None) -> List[Dict[str, Any]]:
        """Search knowledge base"""
        return self.rag_service.search(query, topic)
    
    def get_context(self, policy_id: str) -> Dict[str, Any]:
        """Get contextual information for policy"""
        return self.rag_service.get_context(policy_id)
    
    def call_mcp_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Call MCP tool"""
        return self.mcp_server.call_tool(tool_name, parameters)
    
    def list_mcp_tools(self) -> List[Dict[str, Any]]:
        """List available MCP tools"""
        return self.mcp_server.list_tools()