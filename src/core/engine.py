"""Core governance engine with free LLM integration"""

import asyncio
from typing import Dict, Any, Optional
from dataclasses import dataclass
from .config import settings


@dataclass
class ValidationResult:
    is_valid: bool
    score: float
    violations: list
    explanations: list
    risk_score: Optional[float] = None


@dataclass
class PolicyRule:
    id: str
    name: str
    content: str
    parsed_logic: Dict[str, Any]
    metadata: Dict[str, Any]


class GovernanceEngine:
    """Minimal governance engine using free LLMs"""
    
    def __init__(self):
        self.policy_store: Dict[str, PolicyRule] = {}
        self.schema_store: Dict[str, Any] = {}
        self.llm_client = self._init_llm()
    
    def _init_llm(self):
        """Initialize free LLM client"""
        if settings.LLM_PROVIDER == "ollama":
            from ..providers.ollama import OllamaProvider
            return OllamaProvider(
                base_url=settings.LLM_BASE_URL,
                model=settings.LLM_MODEL
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {settings.LLM_PROVIDER}")
    
    async def parse_policy(self, content: str) -> Dict[str, Any]:
        """Parse natural language policy into structured rules"""
        prompt = f"""
        Parse this policy into JSON rules:
        {content}
        
        Return only JSON with structure:
        {{
            "rules": [
                {{
                    "field": "field_name",
                    "type": "validation_type",
                    "constraint": "constraint_value",
                    "required": true/false
                }}
            ]
        }}
        """
        
        response = await self.llm_client.generate(prompt)
        try:
            import json
            return json.loads(response)
        except:
            # Fallback simple parsing
            return {"rules": [{"field": "data", "type": "object", "required": True}]}
    
    async def validate_data(self, policy_id: str, data: Dict[str, Any]) -> ValidationResult:
        """Validate data against policy"""
        if policy_id not in self.policy_store:
            return ValidationResult(False, 0.0, ["Policy not found"], [])
        
        policy = self.policy_store[policy_id]
        violations = []
        explanations = []
        
        # Simple validation logic
        for rule in policy.parsed_logic.get("rules", []):
            field = rule.get("field")
            if rule.get("required") and field not in data:
                violations.append({
                    "field": field,
                    "description": f"Required field '{field}' is missing",
                    "remediation": f"Add '{field}' to the data"
                })
        
        is_valid = len(violations) == 0
        score = 1.0 if is_valid else max(0.0, 1.0 - len(violations) * 0.2)
        
        return ValidationResult(is_valid, score, violations, explanations)
    
    async def shutdown(self):
        """Cleanup resources"""
        if hasattr(self.llm_client, 'close'):
            await self.llm_client.close()