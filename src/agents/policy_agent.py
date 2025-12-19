"""Policy Agent for natural language policy processing"""

import json
import re
from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentMessage, AgentResponse
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)


class PolicyAgent(BaseAgent):
    """Agent for parsing and managing policies"""
    
    def __init__(self, llm_client=None):
        super().__init__("PolicyAgent")
        self.llm_client = llm_client
        self.policies = {}
        
    async def initialize(self):
        """Initialize policy agent"""
        if not self.llm_client:
            from ..providers.ollama import OllamaProvider
            self.llm_client = OllamaProvider(
                base_url=settings.LLM_BASE_URL,
                model=settings.LLM_MODEL
            )
        logger.info("PolicyAgent initialized")
    
    async def process_message(self, message: AgentMessage) -> AgentResponse:
        """Process policy-related messages"""
        try:
            if message.action == "parse_policy":
                return await self._parse_policy(message.payload)
            elif message.action == "validate_policy":
                return await self._validate_policy(message.payload)
            elif message.action == "get_policy":
                return await self._get_policy(message.payload)
            else:
                return AgentResponse(success=False, error=f"Unknown action: {message.action}")
        except Exception as e:
            return AgentResponse(success=False, error=str(e))
    
    async def _parse_policy(self, payload: Dict[str, Any]) -> AgentResponse:
        """Parse natural language policy into structured rules"""
        policy_text = payload.get("policy_text", "")
        
        prompt = f"""
        Parse this compliance policy into structured JSON rules:
        
        Policy: {policy_text}
        
        Extract:
        1. Required fields and their types
        2. Validation constraints
        3. Business rules
        4. Compliance requirements
        
        Return JSON format:
        {{
            "rules": [
                {{
                    "field": "field_name",
                    "type": "string|number|email|phone|date",
                    "required": true/false,
                    "constraints": {{"min": 0, "max": 100}},
                    "validation": "regex_pattern_or_rule"
                }}
            ],
            "business_rules": [
                {{
                    "condition": "if_condition",
                    "action": "then_action",
                    "priority": "high|medium|low"
                }}
            ],
            "compliance": {{
                "jurisdiction": "US|EU|GLOBAL",
                "regulation": "GDPR|CCPA|SOX|etc",
                "risk_level": "high|medium|low"
            }}
        }}
        """
        
        try:
            response = await self.llm_client.generate(prompt)
            parsed_rules = self._extract_json(response)
            
            policy_id = payload.get("policy_id", f"policy_{len(self.policies)}")
            self.policies[policy_id] = {
                "original_text": policy_text,
                "parsed_rules": parsed_rules,
                "created_at": "2024-01-01T00:00:00Z"
            }
            
            return AgentResponse(
                success=True,
                data={
                    "policy_id": policy_id,
                    "parsed_rules": parsed_rules
                }
            )
        except Exception as e:
            logger.error(f"Policy parsing error: {e}")
            return AgentResponse(success=False, error=f"Failed to parse policy: {e}")
    
    async def _validate_policy(self, payload: Dict[str, Any]) -> AgentResponse:
        """Validate policy syntax and completeness"""
        policy_rules = payload.get("rules", {})
        
        issues = []
        
        # Check for required sections
        if "rules" not in policy_rules:
            issues.append("Missing 'rules' section")
        
        if "compliance" not in policy_rules:
            issues.append("Missing 'compliance' section")
        
        # Validate rule structure
        for rule in policy_rules.get("rules", []):
            if "field" not in rule:
                issues.append(f"Rule missing 'field' property: {rule}")
            if "type" not in rule:
                issues.append(f"Rule missing 'type' property: {rule}")
        
        return AgentResponse(
            success=len(issues) == 0,
            data={"issues": issues, "valid": len(issues) == 0}
        )
    
    async def _get_policy(self, payload: Dict[str, Any]) -> AgentResponse:
        """Retrieve policy by ID"""
        policy_id = payload.get("policy_id")
        
        if policy_id in self.policies:
            return AgentResponse(success=True, data=self.policies[policy_id])
        else:
            return AgentResponse(success=False, error="Policy not found")
    
    def _extract_json(self, text: str) -> Dict[str, Any]:
        """Extract JSON from LLM response"""
        try:
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback simple structure
                return {
                    "rules": [{"field": "data", "type": "object", "required": True}],
                    "business_rules": [],
                    "compliance": {"jurisdiction": "GLOBAL", "regulation": "GENERAL", "risk_level": "medium"}
                }
        except json.JSONDecodeError:
            return {
                "rules": [{"field": "data", "type": "object", "required": True}],
                "business_rules": [],
                "compliance": {"jurisdiction": "GLOBAL", "regulation": "GENERAL", "risk_level": "medium"}
            }