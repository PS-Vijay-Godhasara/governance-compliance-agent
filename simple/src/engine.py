"""Simple Governance Engine - File-based validation with optional LLM"""

import json
import os
import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ValidationResult:
    is_valid: bool
    score: float
    violations: List[str]
    explanations: List[str]
    summary: str

class SimpleGovernanceEngine:
    def __init__(self, policies_dir: str = "./policies", use_llm: bool = False):
        self.policies_dir = policies_dir
        self.use_llm = use_llm
        self.policies = {}
        self.llm_service = None
        
        if use_llm:
            try:
                from llm_service import LLMService
                self.llm_service = LLMService()
            except ImportError:
                self.use_llm = False
        
        self._load_policies()
    
    def _load_policies(self):
        """Load policies from JSON files"""
        if not os.path.exists(self.policies_dir):
            os.makedirs(self.policies_dir)
            self._create_default_policies()
        
        for filename in os.listdir(self.policies_dir):
            if filename.endswith('.json'):
                policy_id = filename[:-5]
                with open(os.path.join(self.policies_dir, filename), 'r') as f:
                    self.policies[policy_id] = json.load(f)
    
    def _create_default_policies(self):
        """Create default policies"""
        policies = {
            "customer_onboarding": {
                "name": "Customer Onboarding",
                "rules": [
                    {"field": "email", "type": "email", "required": True},
                    {"field": "age", "type": "integer", "required": True, "min": 18, "max": 120},
                    {"field": "phone", "type": "string", "required": True, "pattern": r"^\+[1-9]\d{1,14}$"}
                ]
            },
            "kyc_validation": {
                "name": "KYC Validation",
                "rules": [
                    {"field": "identity_documents", "type": "array", "required": True, "min_items": 1},
                    {"field": "date_of_birth", "type": "date", "required": True}
                ]
            }
        }
        
        for policy_id, policy in policies.items():
            with open(os.path.join(self.policies_dir, f"{policy_id}.json"), 'w') as f:
                json.dump(policy, f, indent=2)
    
    def validate(self, policy_id: str, data: Dict[str, Any]) -> ValidationResult:
        """Validate data against policy"""
        if policy_id not in self.policies:
            return ValidationResult(False, 0.0, ["Policy not found"], [], "Policy not found")
        
        policy = self.policies[policy_id]
        violations = []
        score = 1.0
        
        for rule in policy.get("rules", []):
            field = rule["field"]
            
            # Required field check
            if rule.get("required") and field not in data:
                violations.append(f"Missing required field: {field}")
                score -= 0.2
                continue
            
            if field not in data:
                continue
            
            value = data[field]
            
            # Type validation
            if not self._validate_type(value, rule.get("type")):
                violations.append(f"Invalid type for {field}")
                score -= 0.1
            
            # Constraint validation
            if "min" in rule and isinstance(value, (int, float)) and value < rule["min"]:
                violations.append(f"{field} below minimum {rule['min']}")
                score -= 0.1
            
            if "max" in rule and isinstance(value, (int, float)) and value > rule["max"]:
                violations.append(f"{field} above maximum {rule['max']}")
                score -= 0.1
            
            if "pattern" in rule and isinstance(value, str) and not re.match(rule["pattern"], value):
                violations.append(f"{field} format invalid")
                score -= 0.1
            
            if "min_items" in rule and isinstance(value, list) and len(value) < rule["min_items"]:
                violations.append(f"{field} needs at least {rule['min_items']} items")
                score -= 0.1
        
        score = max(0.0, score)
        is_valid = len(violations) == 0
        
        # Generate explanations
        explanations = []
        summary = ""
        
        if self.use_llm and self.llm_service and violations:
            llm_result = self.llm_service.explain_violations(violations, data, policy["name"])
            explanations = [exp.get("explanation", "") for exp in llm_result.get("explanations", [])]
            summary = llm_result.get("summary", "")
        else:
            explanations = [self._simple_explanation(v) for v in violations]
            summary = f"Validation {'passed' if is_valid else 'failed'} with {len(violations)} issues"
        
        return ValidationResult(is_valid, score, violations, explanations, summary)
    
    def _validate_type(self, value: Any, expected_type: str) -> bool:
        """Validate data type"""
        type_map = {
            "string": str,
            "integer": int,
            "number": (int, float),
            "array": list,
            "object": dict,
            "boolean": bool,
            "email": str,
            "date": str
        }
        
        expected = type_map.get(expected_type, str)
        if not isinstance(value, expected):
            return False
        
        # Email validation
        if expected_type == "email":
            return "@" in value and "." in value.split("@")[-1]
        
        return True
    
    def _simple_explanation(self, violation: str) -> str:
        """Generate simple explanation for violation"""
        explanations = {
            "Missing required field": "This field is mandatory and must be provided",
            "Invalid type": "The data format is incorrect",
            "below minimum": "Value is too low",
            "above maximum": "Value is too high",
            "format invalid": "Format does not match requirements"
        }
        
        for key, explanation in explanations.items():
            if key.lower() in violation.lower():
                return explanation
        
        return "Please correct this field"
    
    def create_policy_from_text(self, policy_text: str, policy_id: str) -> Dict[str, Any]:
        """Create policy from natural language"""
        if self.use_llm and self.llm_service:
            policy = self.llm_service.interpret_policy(policy_text)
            policy["policy_id"] = policy_id
            
            # Save policy
            with open(os.path.join(self.policies_dir, f"{policy_id}.json"), 'w') as f:
                json.dump(policy, f, indent=2)
            
            self.policies[policy_id] = policy
            return policy
        
        return {"error": "LLM service not available"}
    
    def get_policy(self, policy_id: str) -> Dict[str, Any]:
        """Get policy by ID"""
        return self.policies.get(policy_id, {})
    
    def list_policies(self) -> List[str]:
        """List available policies"""
        return list(self.policies.keys())