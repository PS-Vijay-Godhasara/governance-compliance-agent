"""Simplified orchestrator for governance workflows"""

from typing import Dict, Any
from ..core.simple_engine import SimpleGovernanceEngine, ValidationResult


class SimpleOrchestrator:
    """Simplified orchestrator without complex agent communication"""
    
    def __init__(self, policies_dir: str = "./policies"):
        self.engine = SimpleGovernanceEngine(policies_dir)
    
    def validate(self, policy_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data against policy"""
        result = self.engine.validate_data(policy_id, data)
        
        # Add simple explanations for violations
        explanations = []
        for violation in result.violations:
            explanation = self._generate_explanation(violation)
            explanations.append(explanation)
        
        return {
            "is_valid": result.is_valid,
            "score": result.score,
            "violations": result.violations,
            "explanations": explanations,
            "policy_name": result.policy_name
        }
    
    def validate_kyc(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Simplified KYC validation"""
        result = self.engine.validate_data("kyc_validation", customer_data)
        
        # Simple KYC scoring
        kyc_score = result.score
        if kyc_score >= 0.8:
            status = "approved"
        elif kyc_score >= 0.5:
            status = "review_required"
        else:
            status = "rejected"
        
        return {
            "kyc_status": status,
            "kyc_score": kyc_score,
            "issues": result.violations,
            "recommendation": self._get_kyc_recommendation(status)
        }
    
    def assess_risk(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Simple risk assessment"""
        risk_score = 0.0
        risk_factors = []
        
        # Transaction amount risk
        if "transaction_amount" in data:
            amount = float(data["transaction_amount"])
            if amount > 10000:
                risk_score += 0.4
                risk_factors.append({"factor": "high_value_transaction", "weight": 0.4})
            elif amount > 5000:
                risk_score += 0.2
                risk_factors.append({"factor": "medium_value_transaction", "weight": 0.2})
        
        # Geographic risk
        if "country" in data and data["country"] in ["XX", "YY"]:  # High-risk countries
            risk_score += 0.3
            risk_factors.append({"factor": "high_risk_geography", "weight": 0.3})
        
        # Age risk
        if "age" in data and data["age"] < 21:
            risk_score += 0.1
            risk_factors.append({"factor": "young_customer", "weight": 0.1})
        
        # Determine risk level
        if risk_score >= 0.7:
            risk_level = "high"
        elif risk_score >= 0.3:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return {
            "risk_level": risk_level,
            "risk_score": min(1.0, risk_score),
            "risk_factors": risk_factors,
            "recommendation": self._get_risk_recommendation(risk_level)
        }
    
    def get_policy(self, policy_id: str) -> Dict[str, Any]:
        """Get policy details"""
        return self.engine.get_policy(policy_id)
    
    def list_policies(self) -> List[str]:
        """List available policies"""
        return self.engine.list_policies()
    
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