"""Agent orchestrator for governance workflows"""

import uuid
import asyncio
from typing import Dict, Any
from ..core.engine import GovernanceEngine, PolicyRule, ValidationResult
from .policy_agent import PolicyAgent
from .rag_agent import RAGAgent
from .validation_agent import ValidationAgent
from .schema_agent import SchemaAgent
from .explanation_agent import ExplanationAgent
from .base_agent import AgentMessage
import logging

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """Multi-agent orchestrator for governance workflows"""
    
    def __init__(self, engine: GovernanceEngine):
        self.engine = engine
        self.agents = {}
        self.initialize_agents()
    
    def initialize_agents(self):
        """Initialize all agents"""
        self.agents = {
            "policy": PolicyAgent(),
            "rag": RAGAgent(),
            "validation": ValidationAgent(),
            "schema": SchemaAgent(),
            "explanation": ExplanationAgent()
        }
        logger.info("All agents initialized")
    
    async def start_agents(self):
        """Start all agents"""
        for agent in self.agents.values():
            await agent.initialize()
        logger.info("All agents started")
    
    async def register_policy(self, name: str, content: str, metadata: Dict[str, Any] = None) -> str:
        """Register a new policy using Policy Agent"""
        policy_id = str(uuid.uuid4())
        
        # Use Policy Agent to parse policy
        message = AgentMessage(
            sender="orchestrator",
            recipient="policy",
            action="parse_policy",
            payload={"policy_text": content, "policy_id": policy_id}
        )
        
        response = await self.agents["policy"].process_message(message)
        
        if response.success:
            # Store in RAG for future retrieval
            rag_message = AgentMessage(
                sender="orchestrator",
                recipient="rag",
                action="store_knowledge",
                payload={
                    "content": content,
                    "type": "policy",
                    "id": policy_id,
                    "metadata": {"name": name, **(metadata or {})}
                }
            )
            await self.agents["rag"].process_message(rag_message)
            
            return policy_id
        else:
            raise ValueError(f"Failed to register policy: {response.error}")
    
    async def validate(self, policy_id: str, data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Comprehensive validation using multiple agents"""
        try:
            # Get policy from Policy Agent
            policy_message = AgentMessage(
                sender="orchestrator",
                recipient="policy",
                action="get_policy",
                payload={"policy_id": policy_id}
            )
            policy_response = await self.agents["policy"].process_message(policy_message)
            
            if not policy_response.success:
                return {"success": False, "error": "Policy not found"}
            
            policy_data = policy_response.data
            rules = policy_data.get("parsed_rules", {})
            
            # Validate data using Validation Agent
            validation_message = AgentMessage(
                sender="orchestrator",
                recipient="validation",
                action="validate_data",
                payload={"data": data, "rules": rules, "context": context or {}}
            )
            validation_response = await self.agents["validation"].process_message(validation_message)
            
            if not validation_response.success:
                return {"success": False, "error": validation_response.error}
            
            validation_result = validation_response.data
            
            # If there are violations, get explanations
            if validation_result.get("violations"):
                explanation_message = AgentMessage(
                    sender="orchestrator",
                    recipient="explanation",
                    action="explain_violation",
                    payload={
                        "violations": validation_result["violations"],
                        "context": context or {},
                        "policy_name": policy_data.get("name", "Unknown Policy")
                    }
                )
                explanation_response = await self.agents["explanation"].process_message(explanation_message)
                
                if explanation_response.success:
                    validation_result["explanations"] = explanation_response.data["explanations"]
                    validation_result["remediation"] = explanation_response.data.get("next_steps", [])
            
            return {"success": True, "data": validation_result}
            
        except Exception as e:
            logger.error(f"Validation orchestration error: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_policy(self, policy_id: str) -> Dict[str, Any]:
        """Get policy by ID using Policy Agent"""
        message = AgentMessage(
            sender="orchestrator",
            recipient="policy",
            action="get_policy",
            payload={"policy_id": policy_id}
        )
        response = await self.agents["policy"].process_message(message)
        
        if response.success:
            return response.data
        else:
            raise ValueError(f"Policy {policy_id} not found")
    
    async def detect_schema_drift(self, old_schema: Dict, new_schema: Dict) -> Dict[str, Any]:
        """Detect schema changes using Schema Agent"""
        message = AgentMessage(
            sender="orchestrator",
            recipient="schema",
            action="detect_drift",
            payload={"old_schema": old_schema, "new_schema": new_schema}
        )
        response = await self.agents["schema"].process_message(message)
        
        if response.success:
            return response.data
        else:
            raise ValueError(f"Schema drift detection failed: {response.error}")
    
    async def perform_kyc_validation(self, customer_data: Dict[str, Any], requirements: Dict[str, Any] = None) -> Dict[str, Any]:
        """Perform KYC validation using Validation Agent"""
        message = AgentMessage(
            sender="orchestrator",
            recipient="validation",
            action="kyc_validation",
            payload={"customer_data": customer_data, "requirements": requirements or {}}
        )
        response = await self.agents["validation"].process_message(message)
        
        if response.success:
            return response.data
        else:
            raise ValueError(f"KYC validation failed: {response.error}")
    
    async def assess_risk(self, data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Perform risk assessment using Validation Agent"""
        message = AgentMessage(
            sender="orchestrator",
            recipient="validation",
            action="risk_assessment",
            payload={"data": data, "context": context or {}}
        )
        response = await self.agents["validation"].process_message(message)
        
        if response.success:
            # Get risk explanation
            explanation_message = AgentMessage(
                sender="orchestrator",
                recipient="explanation",
                action="risk_explanation",
                payload={"risk_assessment": response.data, "context": context or {}}
            )
            explanation_response = await self.agents["explanation"].process_message(explanation_message)
            
            result = response.data
            if explanation_response.success:
                result["explanation"] = explanation_response.data
            
            return result
        else:
            raise ValueError(f"Risk assessment failed: {response.error}")
    
    async def search_knowledge(self, query: str, doc_type: str = "policy", limit: int = 5) -> Dict[str, Any]:
        """Search knowledge base using RAG Agent"""
        message = AgentMessage(
            sender="orchestrator",
            recipient="rag",
            action="retrieve_context",
            payload={"query": query, "type": doc_type, "limit": limit}
        )
        response = await self.agents["rag"].process_message(message)
        
        if response.success:
            return response.data
        else:
            raise ValueError(f"Knowledge search failed: {response.error}")
    
    async def shutdown(self):
        """Shutdown all agents"""
        for agent in self.agents.values():
            await agent.stop()
        logger.info("All agents shutdown complete")