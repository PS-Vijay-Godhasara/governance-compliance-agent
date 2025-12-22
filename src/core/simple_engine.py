"""Simplified governance engine with file-based policies"""

import json
import os
from typing import Dict, Any, List
from dataclasses import dataclass
from .llm_service import LLMService


@dataclass
class ValidationResult:
    is_valid: bool
    score: float
    violations: List[Dict[str, Any]]
    policy_name: str
    explanations: List[str] = None
    natural_language_summary: str = ""


class SimpleGovernanceEngine:
    """Simplified governance engine using file-based policies"""
    
    def __init__(self, policies_dir: str = "./policies", use_llm: bool = True):
        self.policies_dir = policies_dir
        self.policies = {}
        self.use_llm = use_llm
        self.llm_service = LLMService() if use_llm else None
        self._load_policies()
    
    def _load_policies(self):
        """Load policies from JSON files"""
        if not os.path.exists(self.policies_dir):
            os.makedirs(self.policies_dir)
            self._create_sample_policies()
        
        for filename in os.listdir(self.policies_dir):
            if filename.endswith('.json'):
                policy_id = filename[:-5]  # Remove .json extension
                with open(os.path.join(self.policies_dir, filename), 'r') as f:
                    self.policies[policy_id] = json.load(f)
    
    def _create_sample_policies(self):
        """Create sample policies"""
        sample_policies = {
            "customer_onboarding": {
                "name": "Customer Onboarding Policy",
                "rules": [
                    {"field": "email", "type": "email", "required": True},
                    {"field": "age", "type": "integer", "required": True, "min": 18},
                    {"field": "phone", "type": "string", "required": True}
                ]
            },
            "kyc_validation": {
                "name": "KYC Validation Policy", 
                "rules": [
                    {"field": "identity_documents", "type": "array", "required": True, "min_items": 1},
                    {"field": "address_proof", "type": "object", "required": True},
                    {"field": "date_of_birth", "type": "string", "required": True}
                ]
            }
        }
        
        for policy_id, policy_data in sample_policies.items():
            with open(os.path.join(self.policies_dir, f"{policy_id}.json"), 'w') as f:
                json.dump(policy_data, f, indent=2)
    
    def validate_data(self, policy_id: str, data: Dict[str, Any]) -> ValidationResult:
        """Validate data against policy"""
        if policy_id not in self.policies:
            return ValidationResult(False, 0.0, [{"error": "Policy not found"}], "Unknown", [], "Policy not found")
        
        policy = self.policies[policy_id]
        violations = []
        score = 1.0
        
        for rule in policy.get("rules", []):
            field = rule["field"]
            
            # Check required fields
            if rule.get("required", False) and field not in data:
                violations.append({
                    "field": field,
                    "type": "missing_required",
                    "message": f"Required field '{field}' is missing"
                })
                score -= 0.2
                continue
            
            if field not in data:
                continue
            
            value = data[field]
            
            # Type validation
            if not self._validate_type(value, rule.get("type")):
                violations.append({
                    "field": field,
                    "type": "invalid_type", 
                    "message": f"Field '{field}' has invalid type"
                })
                score -= 0.1
            
            # Constraint validation
            if "min" in rule and isinstance(value, (int, float)) and value < rule["min"]:
                violations.append({
                    "field": field,
                    "type": "constraint_violation",
                    "message": f"Field '{field}' value {value} is below minimum {rule['min']}"
                })
                score -= 0.1
            
            if "min_items" in rule and isinstance(value, list) and len(value) < rule["min_items"]:
                violations.append({
                    "field": field,
                    "type": "constraint_violation", 
                    "message": f"Field '{field}' must have at least {rule['min_items']} items"
                })
                score -= 0.1
        
        score = max(0.0, score)
        is_valid = len(violations) == 0
        
        # Generate natural language explanations if LLM is available
        explanations = []
        natural_summary = ""
        
        if self.use_llm and self.llm_service and violations:
            violation_messages = [v["message"] for v in violations]
            llm_explanation = self.llm_service.explain_violations(
                violation_messages, data, policy["name"]
            )
            explanations = [exp["explanation"] for exp in llm_explanation.get("explanations", [])]
            natural_summary = llm_explanation.get("summary", "")
        elif is_valid:
            natural_summary = f"All validation rules passed for {policy['name']}"
        else:
            natural_summary = f"Found {len(violations)} validation issues"
        
        return ValidationResult(is_valid, score, violations, policy["name"], explanations, natural_summary)
    
    def _validate_type(self, value: Any, expected_type: str) -> bool:
        """Simple type validation"""
        type_map = {
            "string": str,
            "integer": int,
            "number": (int, float),
            "array": list,
            "object": dict,
            "boolean": bool,
            "email": str  # Simplified - just check if string
        }
        
        expected = type_map.get(expected_type, str)
        return isinstance(value, expected)
    
    def get_policy(self, policy_id: str) -> Dict[str, Any]:
        """Get policy by ID"""
        return self.policies.get(policy_id, {})
    
    def list_policies(self) -> List[str]:
        """List available policies"""
        return list(self.policies.keys())
    
    def create_policy_from_text(self, policy_text: str, policy_id: str) -> Dict[str, Any]:
        """Create policy from natural language text using LLM"""
        if not self.use_llm or not self.llm_service:
            return {"error": "LLM service not available"}
        
        policy_structure = self.llm_service.interpret_policy(policy_text)
        policy_structure["policy_id"] = policy_id
        
        # Save policy to file
        policy_file = os.path.join(self.policies_dir, f"{policy_id}.json")
        with open(policy_file, 'w') as f:
            json.dump(policy_structure, f, indent=2)
        
        # Add to loaded policies
        self.policies[policy_id] = policy_structure
        
        return policy_structure
    
    def explain_policy(self, policy_id: str) -> str:
        """Get natural language explanation of policy"""
        if policy_id not in self.policies:
            return "Policy not found"
        
        policy = self.policies[policy_id]
        
        if not self.use_llm or not self.llm_service:
            # Fallback explanation
            rules_count = len(policy.get("rules", []))
            return f"Policy '{policy.get('name', policy_id)}' contains {rules_count} validation rules."
        
        # Use LLM for detailed explanation
        prompt = f"Explain this policy in simple business terms: {json.dumps(policy, indent=2)}"
        return self.llm_service._call_ollama(prompt)