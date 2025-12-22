"""Simplified orchestrator for governance workflows"""

from typing import Dict, Any, List
from ..core.simple_engine import SimpleGovernanceEngine, ValidationResult
from ..core.llm_service import LLMService


class SimpleOrchestrator:
    """Simplified orchestrator without complex agent communication"""
    
    def __init__(self, engine: SimpleGovernanceEngine = None, use_llm: bool = True):
        self.engine = engine or SimpleGovernanceEngine(use_llm=use_llm)
        self.use_llm = use_llm
        self.llm_service = LLMService() if use_llm else None
    
    def validate(self, policy_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data against policy"""
        result = self.engine.validate_data(policy_id, data)
        
        return {
            "is_valid": result.is_valid,
            "score": result.score,
            "violations": [v["message"] for v in result.violations],
            "explanations": result.explanations or [],
            "policy_name": result.policy_name,
            "natural_language_summary": result.natural_language_summary
        }
    
    def perform_kyc_validation(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced KYC validation with LLM analysis"""
        result = self.engine.validate_data("kyc_validation", customer_data)
        
        # Simple KYC scoring
        kyc_score = result.score
        if kyc_score >= 0.8:
            status = "APPROVED"
            risk_level = "LOW"
        elif kyc_score >= 0.5:
            status = "REVIEW_REQUIRED"
            risk_level = "MEDIUM"
        else:
            status = "REJECTED"
            risk_level = "HIGH"
        
        # Use LLM for enhanced analysis if available
        explanation = ""
        if self.use_llm and self.llm_service:
            risk_analysis = self.llm_service.assess_risk_factors(customer_data, {"process": "kyc"})
            explanation = risk_analysis.get("explanation", "")
            if risk_analysis.get("risk_level"):
                risk_level = risk_analysis["risk_level"]
        
        return {
            "kyc_status": status,
            "risk_level": risk_level,
            "documents_verified": len(customer_data.get("identity_documents", [])) > 0,
            "violations": [v["message"] for v in result.violations],
            "explanation": explanation or self._get_kyc_recommendation(status)
        }
    
    def assess_risk(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced risk assessment with LLM analysis"""
        # Use LLM for intelligent risk assessment if available
        if self.use_llm and self.llm_service:
            return self.llm_service.assess_risk_factors(data)
        
        # Fallback to simple rule-based assessment
        risk_score = 0.0
        risk_factors = []
        
        # Transaction amount risk
        amount = data.get("amount", data.get("transaction_amount", 0))
        if amount > 10000:
            risk_score += 0.4
            risk_factors.append("High transaction amount")
        elif amount > 5000:
            risk_score += 0.2
            risk_factors.append("Medium transaction amount")
        
        # Geographic risk
        if data.get("country") in ["XX", "YY"]:
            risk_score += 0.3
            risk_factors.append("High-risk country")
        
        # Age risk
        if data.get("age", 25) < 21:
            risk_score += 0.1
            risk_factors.append("Young customer")
        
        # Determine risk level
        if risk_score >= 0.7:
            risk_level = "HIGH"
        elif risk_score >= 0.3:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        return {
            "risk_level": risk_level,
            "risk_score": min(1.0, risk_score),
            "risk_factors": risk_factors,
            "requires_approval": risk_score >= 0.5,
            "explanation": self._get_risk_recommendation(risk_level)
        }
    
    def get_policy(self, policy_id: str) -> Dict[str, Any]:
        """Get policy details"""
        return self.engine.get_policy(policy_id)
    
    def list_policies(self) -> List[str]:
        """List available policies"""
        return self.engine.list_policies()
    
    def create_policy_from_text(self, policy_text: str, policy_id: str) -> Dict[str, Any]:
        """Create policy from natural language description"""
        return self.engine.create_policy_from_text(policy_text, policy_id)
    
    def explain_policy(self, policy_id: str) -> str:
        """Get natural language explanation of policy"""
        return self.engine.explain_policy(policy_id)
    
    def generate_compliance_report(self, validation_results: List[Dict[str, Any]]) -> str:
        """Generate natural language compliance report"""
        if self.use_llm and self.llm_service:
            return self.llm_service.generate_compliance_report(validation_results)
        
        # Fallback simple report
        total = len(validation_results)
        passed = sum(1 for r in validation_results if r.get("is_valid", False))
        return f"Compliance Report: {passed}/{total} validations passed. {total-passed} issues found."
    
    def _generate_explanation(self, violation: Dict[str, Any]) -> Dict[str, Any]:
        """Generate simple explanation for violation"""
        field = violation.get("field", "unknown")
        violation_type = violation.get("type", "unknown")
        
        explanations = {
            "missing_required": f"The field '{field}' is required but was not provided. Please include this information.",
            "invalid_type": f"The field '{field}' has an incorrect data type. Please check the format.",
            "constraint_violation": f"The field '{field}' does not meet the required constraints."
        }
        
        return {
            "field": field,
            "violation_type": violation_type,
            "explanation": explanations.get(violation_type, f"Issue with field '{field}'"),
            "remediation": f"Please correct the '{field}' field and try again"
        }
    
    def _get_kyc_recommendation(self, status: str) -> str:
        """Get KYC recommendation"""
        recommendations = {
            "approved": "Customer approved for onboarding",
            "rejected": "Customer rejected - critical issues found",
            "review_required": "Manual review required - resolve identified issues"
        }
        return recommendations.get(status, "Unknown status")
    
    def _get_risk_recommendation(self, risk_level: str) -> str:
        """Get risk recommendation"""
        recommendations = {
            "low": "Standard processing approved",
            "medium": "Enhanced monitoring recommended", 
            "high": "Manual review and approval required"
        }
        return recommendations.get(risk_level, "Unknown risk level")