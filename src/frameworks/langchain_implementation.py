"""LangChain-based implementation of governance agents"""

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_ollama import ChatOllama
from langchain.tools import BaseTool
from langchain.agents import AgentExecutor, create_openai_functions_agent
from typing import Dict, Any, List
import json


class PolicyParsingTool(BaseTool):
    """Tool for parsing natural language policies"""
    name = "policy_parser"
    description = "Parse natural language policy into structured rules"
    
    def _run(self, policy_text: str) -> str:
        # Simplified parsing logic
        rules = {
            "rules": [
                {"field": "email", "type": "email", "required": True},
                {"field": "age", "type": "integer", "required": True, "constraints": {"min": 18}}
            ]
        }
        return json.dumps(rules)


class DataValidationTool(BaseTool):
    """Tool for validating data against rules"""
    name = "data_validator"
    description = "Validate data against policy rules"
    
    def _run(self, data: str, rules: str) -> str:
        data_dict = json.loads(data)
        rules_dict = json.loads(rules)
        
        violations = []
        for rule in rules_dict.get("rules", []):
            field = rule.get("field")
            if rule.get("required") and field not in data_dict:
                violations.append({
                    "field": field,
                    "type": "missing_required",
                    "severity": "high"
                })
        
        result = {
            "is_valid": len(violations) == 0,
            "violations": violations,
            "score": 1.0 if len(violations) == 0 else 0.5
        }
        return json.dumps(result)


class RiskAssessmentTool(BaseTool):
    """Tool for risk assessment"""
    name = "risk_assessor"
    description = "Assess risk level of data or transaction"
    
    def _run(self, data: str) -> str:
        data_dict = json.loads(data)
        
        risk_score = 0.0
        risk_factors = []
        
        if "transaction_amount" in data_dict and data_dict["transaction_amount"] > 10000:
            risk_score += 0.3
            risk_factors.append({"factor": "high_value", "weight": 0.3})
        
        risk_level = "high" if risk_score >= 0.8 else "medium" if risk_score >= 0.5 else "low"
        
        result = {
            "risk_level": risk_level,
            "risk_score": risk_score,
            "risk_factors": risk_factors
        }
        return json.dumps(result)


class LangChainGovernanceAgent:
    """LangChain-based governance agent system"""
    
    def __init__(self):
        self.llm = ChatOllama(model="mistral:7b")
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        self.tools = [
            PolicyParsingTool(),
            DataValidationTool(),
            RiskAssessmentTool()
        ]
        self._setup_chains()
    
    def _setup_chains(self):
        """Setup LangChain chains"""
        
        # Policy parsing chain
        policy_prompt = PromptTemplate(
            input_variables=["policy_text"],
            template="""
            Parse this compliance policy into structured JSON rules:
            
            Policy: {policy_text}
            
            Extract field requirements, data types, and constraints.
            Return only valid JSON.
            """
        )
        self.policy_chain = LLMChain(
            llm=self.llm,
            prompt=policy_prompt,
            memory=self.memory
        )
        
        # Explanation chain
        explanation_prompt = PromptTemplate(
            input_variables=["violations", "context"],
            template="""
            Explain these policy violations in business terms:
            
            Violations: {violations}
            Context: {context}
            
            Provide clear explanations and remediation steps.
            """
        )
        self.explanation_chain = LLMChain(
            llm=self.llm,
            prompt=explanation_prompt
        )
    
    async def parse_policy(self, policy_text: str) -> Dict[str, Any]:
        """Parse natural language policy"""
        try:
            result = await self.policy_chain.arun(policy_text=policy_text)
            return json.loads(result)
        except:
            # Fallback
            return {
                "rules": [
                    {"field": "email", "type": "email", "required": True},
                    {"field": "age", "type": "integer", "required": True}
                ]
            }
    
    async def validate_data(self, data: Dict[str, Any], rules: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data against rules"""
        tool = DataValidationTool()
        result = tool._run(json.dumps(data), json.dumps(rules))
        return json.loads(result)
    
    async def assess_risk(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess risk level"""
        tool = RiskAssessmentTool()
        result = tool._run(json.dumps(data))
        return json.loads(result)
    
    async def explain_violations(self, violations: List[Dict], context: Dict = None) -> str:
        """Generate explanations for violations"""
        return await self.explanation_chain.arun(
            violations=json.dumps(violations),
            context=json.dumps(context or {})
        )
    
    async def process_governance_request(self, policy_text: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process complete governance workflow"""
        
        # Step 1: Parse policy
        parsed_rules = await self.parse_policy(policy_text)
        
        # Step 2: Validate data
        validation_result = await self.validate_data(data, parsed_rules)
        
        # Step 3: Assess risk
        risk_assessment = await self.assess_risk(data)
        
        # Step 4: Generate explanations if needed
        explanations = None
        if not validation_result["is_valid"]:
            explanations = await self.explain_violations(
                validation_result["violations"],
                {"policy": policy_text}
            )
        
        # Step 5: Make decision
        is_valid = validation_result["is_valid"]
        risk_level = risk_assessment["risk_level"]
        
        if is_valid and risk_level in ["low", "medium"]:
            decision = "approved"
        elif is_valid and risk_level == "high":
            decision = "manual_review"
        else:
            decision = "rejected"
        
        return {
            "decision": decision,
            "parsed_rules": parsed_rules,
            "validation_result": validation_result,
            "risk_assessment": risk_assessment,
            "explanations": explanations
        }


# Usage example
async def main():
    agent = LangChainGovernanceAgent()
    
    policy = "All customers must provide valid email and be over 18 years old"
    customer_data = {
        "email": "john@example.com",
        "age": 25,
        "transaction_amount": 15000
    }
    
    result = await agent.process_governance_request(policy, customer_data)
    print(f"Decision: {result['decision']}")
    print(f"Risk Level: {result['risk_assessment']['risk_level']}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())