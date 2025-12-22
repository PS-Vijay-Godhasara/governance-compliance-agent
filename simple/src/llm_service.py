"""Simple LLM Service for Natural Language Processing"""

import json
import requests
from typing import Dict, List, Any

class LLMService:
    def __init__(self, model: str = "llama3.2:3b", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
    
    def _call_llm(self, prompt: str) -> str:
        """Call LLM API"""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.1}
                },
                timeout=30
            )
            if response.status_code == 200:
                return response.json().get("response", "")
            return "LLM unavailable"
        except Exception:
            return "LLM error"
    
    def interpret_policy(self, policy_text: str) -> Dict[str, Any]:
        """Convert natural language to policy rules"""
        prompt = f"""Convert this policy to JSON rules:

{policy_text}

Format:
{{
  "name": "Policy Name",
  "rules": [
    {{"field": "fieldname", "type": "string|integer|email", "required": true, "min": 0}}
  ],
  "description": "Brief description"
}}

JSON:"""
        
        response = self._call_llm(prompt)
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except:
            pass
        
        return {
            "name": "Generated Policy",
            "rules": [{"field": "data", "type": "string", "required": True}],
            "description": "Policy interpretation failed"
        }
    
    def explain_violations(self, violations: List[str], data: Dict[str, Any], policy_name: str) -> Dict[str, Any]:
        """Generate explanations for violations"""
        prompt = f"""Explain these validation errors in simple terms:

Policy: {policy_name}
Violations: {violations}
Data: {json.dumps(data)}

Format:
{{
  "summary": "Brief summary",
  "explanations": [
    {{"violation": "error", "explanation": "why this matters", "fix": "how to fix"}}
  ]
}}

JSON:"""
        
        response = self._call_llm(prompt)
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except:
            pass
        
        return {
            "summary": f"Found {len(violations)} issues",
            "explanations": [{"violation": v, "explanation": "Please fix this issue", "fix": "Correct the data"} for v in violations]
        }
    
    def assess_risk(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess risk factors"""
        prompt = f"""Analyze risk for this data:

{json.dumps(data)}

Format:
{{
  "risk_level": "LOW|MEDIUM|HIGH",
  "risk_score": 0.5,
  "risk_factors": ["factor1", "factor2"],
  "requires_approval": true,
  "explanation": "risk analysis"
}}

JSON:"""
        
        response = self._call_llm(prompt)
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                result = json.loads(response[start:end])
                if isinstance(result.get("risk_score"), str):
                    result["risk_score"] = 0.5
                return result
        except:
            pass
        
        return {
            "risk_level": "MEDIUM",
            "risk_score": 0.5,
            "risk_factors": ["Unable to analyze"],
            "requires_approval": True,
            "explanation": "Risk analysis unavailable"
        }