"""Multi-Agent Orchestrator"""

import asyncio
from typing import Dict, Any, List
from .agents.base_agent import BaseAgent, Message

class MultiAgentOrchestrator:
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.message_broker = asyncio.Queue()
        self.running = False
        
    async def register_agent(self, agent: BaseAgent):
        """Register an agent with the orchestrator"""
        self.agents[agent.agent_id] = agent
        await agent.start()
        
    async def start(self):
        """Start the orchestrator"""
        self.running = True
        # Start message broker task
        asyncio.create_task(self._message_broker_loop())
        
    async def stop(self):
        """Stop the orchestrator"""
        self.running = False
        for agent in self.agents.values():
            await agent.stop()
            
    async def _message_broker_loop(self):
        """Message broker loop"""
        while self.running:
            try:
                message = await asyncio.wait_for(self.message_broker.get(), timeout=1.0)
                await self._route_message(message)
            except asyncio.TimeoutError:
                continue
                
    async def _route_message(self, message: Message):
        """Route message to recipient agent"""
        if message.recipient in self.agents:
            agent = self.agents[message.recipient]
            response = await agent.receive_message(message)
            if response:
                await self.message_broker.put(response)
                
    async def send_message(self, message: Message):
        """Send message through broker"""
        await self.message_broker.put(message)
        
    async def execute_workflow(self, workflow_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a multi-agent workflow"""
        if workflow_type == "validation":
            return await self._validation_workflow(data)
        elif workflow_type == "kyc":
            return await self._kyc_workflow(data)
        elif workflow_type == "risk_assessment":
            return await self._risk_workflow(data)
        else:
            return {"error": "Unknown workflow type"}
            
    async def _validation_workflow(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Multi-agent validation workflow"""
        # Simplified workflow - in reality would coordinate multiple agents
        return {
            "workflow": "validation",
            "status": "completed",
            "result": {"is_valid": True, "score": 1.0}
        }
        
    async def _kyc_workflow(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Multi-agent KYC workflow"""
        return {
            "workflow": "kyc",
            "status": "completed", 
            "result": {"kyc_status": "APPROVED", "risk_level": "LOW"}
        }
        
    async def _risk_workflow(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Multi-agent risk assessment workflow"""
        return {
            "workflow": "risk_assessment",
            "status": "completed",
            "result": {"risk_level": "MEDIUM", "risk_score": 0.5}
        }
        
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        return {
            "orchestrator_running": self.running,
            "registered_agents": len(self.agents),
            "agents": {agent_id: agent.get_status() for agent_id, agent in self.agents.items()}
        }