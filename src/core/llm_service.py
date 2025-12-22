"""
LLM Service for Natural Language Policy Processing
Provides LLM-powered policy interpretation and explanations
"""

import json
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime

class LLMService:
    def __init__(self, provider: str = "ollama", model: str = "llama3.2:3b", base_url: str = "http://localhost:11434"):
        self.provider = provider
        self.model = model
        self.base_url = base_url
        
    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama API"""
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
            return "LLM service unavailable"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def interpret_policy(self, policy_text: str) -> Dict[str, Any]:
        """Convert natural language policy to structured rules"""
        prompt = f"""
Convert this natural language policy into structured validation rules:

Policy: {policy_text}

Return a JSON object with these fields:
- rules: array of validation rules with field, type, required, constraints
- description: brief policy summary
- risk_level: LOW/MEDIUM/HIGH

Example format:
{{
  "rules": [
    {{"field": "age", "type": "integer", "required": true, "min": 18, "description": "Must be 18 or older"}}
  ],
  "description": "Age verification policy",
  "risk_level": "MEDIUM"
}}

JSON:"""
        
        response = self._call_ollama(prompt)
        try:
            # Extract JSON from response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except:
            pass
        
        # Fallback response
        return {
            "rules": [{"field": "data", "type": "any", "required": true, "description": "Data validation required"}],
            "description": "Policy interpretation failed",
            "risk_level": "HIGH"
        }
    
    def explain_violations(self, violations: List[str], data: Dict[str, Any], policy_name: str) -> Dict[str, Any]:
        """Generate natural language explanations for violations"""
        prompt = f"""
Explain these data validation violations in simple business terms:

Policy: {policy_name}
Data: {json.dumps(data, indent=2)}
Violations: {violations}

Provide:
1. Clear explanation of each violation
2. Business impact
3. How to fix each issue
4. Overall risk assessment

Format as JSON:
{{
  "summary": "Brief overall summary",
  "explanations": [
    {{"violation": "specific violation", "explanation": "why this matters", "fix": "how to resolve"}}
  ],
  "business_impact": "impact description",
  "risk_level": "LOW/MEDIUM/HIGH",
  "next_steps": ["action 1", "action 2"]
}}

JSON:"""
        
        response = self._call_ollama(prompt)
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except:
            pass
        
        # Fallback response
        return {
            "summary": f"Found {len(violations)} validation issues",
            "explanations": [{"violation": v, "explanation": "Data validation failed", "fix": "Please correct the data"} for v in violations],
            "business_impact": "Data quality issues may affect processing",
            "risk_level": "MEDIUM",
            "next_steps": ["Review and correct data", "Resubmit for validation"]
        }
    
    def assess_risk_factors(self, data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Assess risk factors using LLM analysis"""
        prompt = f"""
Analyze this data for risk factors:

Data: {json.dumps(data, indent=2)}
Context: {json.dumps(context or {}, indent=2)}

Identify potential risks and provide assessment:

Format as JSON:
{{
  "risk_level": "LOW/MEDIUM/HIGH",
  "risk_score": 0.0-1.0,
  "risk_factors": ["factor 1", "factor 2"],
  "recommendations": ["recommendation 1", "recommendation 2"],
  "requires_approval": true/false,
  "explanation": "detailed risk analysis"
}}

JSON:"""
        
        response = self._call_ollama(prompt)
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                result = json.loads(response[start:end])
                # Ensure numeric risk_score
                if "risk_score" in result and isinstance(result["risk_score"], str):
                    try:
                        result["risk_score"] = float(result["risk_score"])
                    except:
                        result["risk_score"] = 0.5
                return result
        except:
            pass
        
        # Fallback response
        return {
            "risk_level": "MEDIUM",
            "risk_score": 0.5,
            "risk_factors": ["Unable to analyze risk factors"],
            "recommendations": ["Manual review recommended"],
            "requires_approval": True,
            "explanation": "Risk analysis unavailable"
        }
    
    def generate_compliance_report(self, validation_results: List[Dict[str, Any]]) -> str:
        """Generate natural language compliance report"""
        prompt = f"""
Generate a compliance report based on these validation results:

Results: {json.dumps(validation_results, indent=2)}

Create a professional report covering:
1. Executive summary
2. Validation results overview
3. Key findings and violations
4. Risk assessment
5. Recommendations

Keep it concise and business-focused.

Report:"""
        
        return self._call_ollama(prompt)
    
    def check_policy_consistency(self, policies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Check for conflicts between multiple policies"""
        prompt = f"""
Analyze these policies for conflicts or inconsistencies:

Policies: {json.dumps(policies, indent=2)}

Identify:
1. Conflicting requirements
2. Overlapping rules
3. Gaps in coverage
4. Recommendations for resolution

Format as JSON:
{{
  "conflicts": [
    {{"policy1": "name", "policy2": "name", "conflict": "description", "severity": "LOW/MEDIUM/HIGH"}}
  ],
  "gaps": ["gap 1", "gap 2"],
  "recommendations": ["recommendation 1", "recommendation 2"],
  "overall_consistency": "GOOD/FAIR/POOR"
}}

JSON:"""
        
        response = self._call_ollama(prompt)
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except:
            pass
        
        return {
            "conflicts": [],
            "gaps": [],
            "recommendations": ["Review policies manually"],
            "overall_consistency": "UNKNOWN"
        }