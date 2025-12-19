"""MCP (Model Context Protocol) Server for agent integration"""

import asyncio
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from ..agents.policy_agent import PolicyAgent
from ..agents.rag_agent import RAGAgent
from ..agents.validation_agent import ValidationAgent
import logging

logger = logging.getLogger(__name__)


@dataclass
class MCPTool:
    """MCP Tool definition"""
    name: str
    description: str
    input_schema: Dict[str, Any]


@dataclass
class MCPResponse:
    """MCP Response format"""
    success: bool
    data: Any
    error: Optional[str] = None


class MCPServer:
    """Model Context Protocol Server for governance agents"""
    
    def __init__(self):
        self.tools = {}
        self.agents = {}
        self.initialize_agents()
        self.register_tools()
    
    def initialize_agents(self):
        """Initialize all agents"""
        self.agents = {
            "policy": PolicyAgent(),
            "rag": RAGAgent(),
            "validation": ValidationAgent()
        }
    
    def register_tools(self):
        """Register MCP tools for each agent"""
        
        # Policy Agent Tools
        self.tools.update({
            "parse_policy": MCPTool(
                name="parse_policy",
                description="Parse natural language policy into structured rules",
                input_schema={
                    "type": "object",
                    "properties": {
                        "policy_text": {"type": "string", "description": "Natural language policy text"},
                        "policy_id": {"type": "string", "description": "Optional policy identifier"}
                    },
                    "required": ["policy_text"]
                }
            ),
            "validate_policy": MCPTool(
                name="validate_policy",
                description="Validate policy structure and completeness",
                input_schema={
                    "type": "object",
                    "properties": {
                        "rules": {"type": "object", "description": "Policy rules to validate"}
                    },
                    "required": ["rules"]
                }
            ),
            "get_policy": MCPTool(
                name="get_policy",
                description="Retrieve policy by ID",
                input_schema={
                    "type": "object",
                    "properties": {
                        "policy_id": {"type": "string", "description": "Policy identifier"}
                    },
                    "required": ["policy_id"]
                }
            )
        })
        
        # RAG Agent Tools
        self.tools.update({
            "store_knowledge": MCPTool(
                name="store_knowledge",
                description="Store knowledge in vector database",
                input_schema={
                    "type": "object",
                    "properties": {
                        "content": {"type": "string", "description": "Content to store"},
                        "type": {"type": "string", "description": "Document type (policy/regulation)"},
                        "id": {"type": "string", "description": "Document identifier"},
                        "metadata": {"type": "object", "description": "Additional metadata"}
                    },
                    "required": ["content"]
                }
            ),
            "retrieve_context": MCPTool(
                name="retrieve_context",
                description="Retrieve relevant context for a query",
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "type": {"type": "string", "description": "Document type to search"},
                        "limit": {"type": "integer", "description": "Maximum results to return"}
                    },
                    "required": ["query"]
                }
            ),
            "semantic_search": MCPTool(
                name="semantic_search",
                description="Perform semantic search across knowledge base",
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "threshold": {"type": "number", "description": "Similarity threshold"}
                    },
                    "required": ["query"]
                }
            )
        })
        
        # Validation Agent Tools
        self.tools.update({
            "validate_data": MCPTool(
                name="validate_data",
                description="Validate data against policy rules",
                input_schema={
                    "type": "object",
                    "properties": {
                        "data": {"type": "object", "description": "Data to validate"},
                        "rules": {"type": "object", "description": "Validation rules"},
                        "context": {"type": "object", "description": "Additional context"}
                    },
                    "required": ["data", "rules"]
                }
            ),
            "kyc_validation": MCPTool(
                name="kyc_validation",
                description="Perform KYC validation",
                input_schema={
                    "type": "object",
                    "properties": {
                        "customer_data": {"type": "object", "description": "Customer data"},
                        "requirements": {"type": "object", "description": "KYC requirements"}
                    },
                    "required": ["customer_data"]
                }
            ),
            "risk_assessment": MCPTool(
                name="risk_assessment",
                description="Perform risk assessment",
                input_schema={
                    "type": "object",
                    "properties": {
                        "data": {"type": "object", "description": "Data for risk assessment"},
                        "context": {"type": "object", "description": "Additional context"}
                    },
                    "required": ["data"]
                }
            ),
            "compliance_check": MCPTool(
                name="compliance_check",
                description="Check compliance against regulations",
                input_schema={
                    "type": "object",
                    "properties": {
                        "data": {"type": "object", "description": "Data to check"},
                        "regulations": {"type": "array", "description": "Regulations to check against"},
                        "jurisdiction": {"type": "string", "description": "Legal jurisdiction"}
                    },
                    "required": ["data", "regulations"]
                }
            )
        })
    
    async def start_server(self, host: str = "localhost", port: int = 8001):
        """Start MCP server"""
        try:
            # Initialize all agents
            for agent in self.agents.values():
                await agent.initialize()
            
            logger.info(f"MCP Server started on {host}:{port}")
            logger.info(f"Available tools: {list(self.tools.keys())}")
            
            # In a real implementation, this would start an HTTP/WebSocket server
            # For now, we'll just keep the server running
            while True:
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"MCP Server error: {e}")
    
    async def call_tool(self, tool_name: str, parameters: Dict[str, Any]) -> MCPResponse:
        """Call a tool through MCP interface"""
        try:
            if tool_name not in self.tools:
                return MCPResponse(
                    success=False,
                    data=None,
                    error=f"Tool '{tool_name}' not found"
                )
            
            # Route to appropriate agent
            if tool_name in ["parse_policy", "validate_policy", "get_policy"]:
                agent = self.agents["policy"]
                action = tool_name
            elif tool_name in ["store_knowledge", "retrieve_context", "semantic_search"]:
                agent = self.agents["rag"]
                action = tool_name
            elif tool_name in ["validate_data", "kyc_validation", "risk_assessment", "compliance_check"]:
                agent = self.agents["validation"]
                action = tool_name
            else:
                return MCPResponse(
                    success=False,
                    data=None,
                    error=f"No agent found for tool '{tool_name}'"
                )
            
            # Create agent message
            from ..agents.base_agent import AgentMessage
            message = AgentMessage(
                sender="mcp_server",
                recipient=agent.name,
                action=action,
                payload=parameters
            )
            
            # Process message
            response = await agent.process_message(message)
            
            return MCPResponse(
                success=response.success,
                data=response.data,
                error=response.error
            )
            
        except Exception as e:
            logger.error(f"Tool call error: {e}")
            return MCPResponse(
                success=False,
                data=None,
                error=str(e)
            )
    
    def get_tools_schema(self) -> List[Dict[str, Any]]:
        """Get schema for all available tools"""
        return [asdict(tool) for tool in self.tools.values()]
    
    async def shutdown(self):
        """Shutdown MCP server and agents"""
        for agent in self.agents.values():
            await agent.stop()
        logger.info("MCP Server shutdown complete")