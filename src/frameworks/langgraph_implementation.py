"""LangGraph-based implementation of governance agents"""

from typing import Dict, Any, List, Optional
from langgraph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from pydantic import BaseModel
import asyncio


class GovernanceState(BaseModel):
    """State for governance workflow"""
    policy_text: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    parsed_rules: Optional[Dict[str, Any]] = None
    validation_result: Optional[Dict[str, Any]] = None
    risk_assessment: Optional[Dict[str, Any]] = None
    explanations: Optional[List[Dict[str, Any]]] = None
    decision: Optional[str] = None
    messages: List[Any] = []


@tool
def parse_policy_tool(policy_text: str) -> Dict[str, Any]:
    """Parse natural language policy into structured rules"""
    return {
        "rules": [
            {"field": "email", "type": "email", "required": True},
            {"field": "age", "type": "integer", "required": True, "constraints": {"min": 18}}
        ]
    }


@tool
def validate_data_tool(data: Dict[str, Any], rules: Dict[str, Any]) -> Dict[str, Any]:
    """Validate data against policy rules"""
    violations = []
    
    for rule in rules.get("rules", []):
        field = rule.get("field")
        if rule.get("required") and field not in data:
            violations.append({
                "field": field,
                "type": "missing_required",
                "severity": "high"
            })
    
    return {
        "is_valid": len(violations) == 0,
        "violations": violations,
        "score": 1.0 if len(violations) == 0 else 0.5
    }


@tool
def assess_risk_tool(data: Dict[str, Any]) -> Dict[str, Any]:
    """Assess risk level"""
    risk_score = 0.0
    risk_factors = []
    
    if "transaction_amount" in data and data["transaction_amount"] > 10000:
        risk_score += 0.3
        risk_factors.append({"factor": "high_value", "weight": 0.3})
    
    risk_level = "high" if risk_score >= 0.8 else "medium" if risk_score >= 0.5 else "low"
    
    return {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "risk_factors": risk_factors
    }


class LangGraphGovernanceAgent:
    """LangGraph-based governance agent system"""
    
    def __init__(self):
        self.llm = ChatOllama(model="mistral:7b")
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the governance workflow graph"""
        workflow = StateGraph(GovernanceState)
        
        # Add nodes
        workflow.add_node("parse_policy", self._parse_policy)
        workflow.add_node("validate_data", self._validate_data)
        workflow.add_node("assess_risk", self._assess_risk)
        workflow.add_node("make_decision", self._make_decision)
        
        # Add edges
        workflow.add_edge("parse_policy", "validate_data")
        workflow.add_edge("validate_data", "assess_risk")
        workflow.add_edge("assess_risk", "make_decision")
        workflow.add_edge("make_decision", END)
        
        workflow.set_entry_point("parse_policy")
        
        return workflow.compile()
    
    def _parse_policy(self, state: GovernanceState) -> GovernanceState:
        """Parse policy node"""
        if state.policy_text:
            state.parsed_rules = parse_policy_tool.invoke({"policy_text": state.policy_text})
        return state
    
    def _validate_data(self, state: GovernanceState) -> GovernanceState:
        """Validate data node"""
        if state.data and state.parsed_rules:
            state.validation_result = validate_data_tool.invoke({
                "data": state.data,
                "rules": state.parsed_rules
            })
        return state
    
    def _assess_risk(self, state: GovernanceState) -> GovernanceState:
        """Assess risk node"""
        if state.data:
            state.risk_assessment = assess_risk_tool.invoke({"data": state.data})
        return state
    
    def _make_decision(self, state: GovernanceState) -> GovernanceState:
        """Make final decision"""
        is_valid = state.validation_result and state.validation_result["is_valid"]
        risk_level = state.risk_assessment and state.risk_assessment["risk_level"]
        
        if is_valid and risk_level in ["low", "medium"]:
            state.decision = "approved"
        elif is_valid and risk_level == "high":
            state.decision = "manual_review"
        else:
            state.decision = "rejected"
        
        return state
    
    async def process(self, policy_text: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process governance request"""
        initial_state = GovernanceState(
            policy_text=policy_text,
            data=data
        )
        
        final_state = await self.graph.ainvoke(initial_state)
        
        return {
            "decision": final_state.decision,
            "validation_result": final_state.validation_result,
            "risk_assessment": final_state.risk_assessment
        }