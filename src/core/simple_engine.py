"""Simplified governance engine with file-based policies"""

import json
import os
from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class ValidationResult:
    is_valid: bool
    score: float
    violations: List[Dict[str, Any]]
    policy_name: str


class SimpleGovernanceEngine:
    """Simplified governance engine using file-based policies"""
    
    def __init__(self, policies_dir: str = "./policies"):
        self.policies_dir = policies_dir
        self.policies = {}
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
            return ValidationResult(False, 0.0, [{"error": "Policy not found"}], "Unknown")
        
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
        
        return ValidationResult(is_valid, score, violations, policy["name"])
    
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