"""Simple MCP Server - Model Context Protocol implementation"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime

class SimpleMCPServer:
    def __init__(self):
        self.tools = {}
        self.resources = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register default governance tools"""
        self.tools = {
            "validate_data": {
                "name": "validate_data",
                "description": "Validate data against governance policy",
                "parameters": {
                    "policy_id": {"type": "string", "required": True},
                    "data": {"type": "object", "required": True}
                }
            },
            "assess_risk": {
                "name": "assess_risk", 
                "description": "Assess risk factors for given data",
                "parameters": {
                    "data": {"type": "object", "required": True}
                }
            },
            "validate_kyc": {
                "name": "validate_kyc",
                "description": "Perform KYC validation workflow",
                "parameters": {
                    "customer_data": {"type": "object", "required": True}
                }
            },
            "search_knowledge": {
                "name": "search_knowledge",
                "description": "Search governance knowledge base",
                "parameters": {
                    "query": {"type": "string", "required": True},
                    "topic": {"type": "string", "required": False}
                }
            },
            "list_policies": {
                "name": "list_policies",
                "description": "List available governance policies",
                "parameters": {}
            },
            "get_policy": {
                "name": "get_policy",
                "description": "Get specific policy details",
                "parameters": {
                    "policy_id": {"type": "string", "required": True}
                }
            },
            "create_policy": {
                "name": "create_policy",
                "description": "Create policy from natural language",
                "parameters": {
                    "policy_text": {"type": "string", "required": True},
                    "policy_id": {"type": "string", "required": True}
                }
            },
            "explain_violation": {
                "name": "explain_violation",
                "description": "Explain policy violations in natural language",
                "parameters": {
                    "violations": {"type": "array", "required": True},
                    "policy_id": {"type": "string", "required": True}
                }
            }
        }
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List available tools"""
        return list(self.tools.values())
    
    def get_tool(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get specific tool definition"""
        return self.tools.get(tool_name)
    
    def call_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool with parameters"""
        if tool_name not in self.tools:
            return {"error": f"Tool '{tool_name}' not found"}
        
        try:
            # Validate parameters
            tool_def = self.tools[tool_name]
            self._validate_parameters(parameters, tool_def["parameters"])
            
            # Execute tool (would integrate with orchestrator in real implementation)
            result = self._execute_tool(tool_name, parameters)
            
            return {
                "tool": tool_name,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            return {"error": str(e)}
    
    def _validate_parameters(self, params: Dict[str, Any], param_def: Dict[str, Any]):
        """Validate tool parameters"""
        for param_name, param_info in param_def.items():
            if param_info.get("required", False) and param_name not in params:
                raise ValueError(f"Required parameter '{param_name}' missing")
    
    def _execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        """Execute tool logic - simplified implementation"""
        if tool_name == "validate_data":
            return {
                "is_valid": True,
                "score": 1.0,
                "violations": [],
                "summary": "Validation passed"
            }
        
        elif tool_name == "assess_risk":
            return {
                "risk_level": "LOW",
                "risk_score": 0.2,
                "risk_factors": [],
                "requires_approval": False
            }
        
        elif tool_name == "validate_kyc":
            return {
                "kyc_status": "APPROVED",
                "risk_level": "LOW",
                "explanation": "KYC validation completed successfully"
            }
        
        elif tool_name == "search_knowledge":
            return {
                "results": [
                    {
                        "topic": "regulations",
                        "content": "Sample regulatory information",
                        "relevance": 0.8
                    }
                ]
            }
        
        elif tool_name == "list_policies":
            return {
                "policies": ["customer_onboarding", "kyc_validation"]
            }
        
        elif tool_name == "get_policy":
            return {
                "policy_id": parameters["policy_id"],
                "name": "Sample Policy",
                "rules": []
            }
        
        elif tool_name == "create_policy":
            return {
                "policy_id": parameters["policy_id"],
                "status": "created",
                "message": "Policy created from natural language"
            }
        
        elif tool_name == "explain_violation":
            return {
                "explanations": [
                    {
                        "violation": v,
                        "explanation": f"Issue with {v}",
                        "fix": "Please correct the data"
                    } for v in parameters["violations"]
                ]
            }
        
        return {"message": "Tool executed successfully"}
    
    def add_resource(self, resource_id: str, resource_data: Dict[str, Any]):
        """Add a resource to the server"""
        self.resources[resource_id] = {
            **resource_data,
            "created_at": datetime.now().isoformat()
        }
    
    def get_resource(self, resource_id: str) -> Optional[Dict[str, Any]]:
        """Get a resource by ID"""
        return self.resources.get(resource_id)
    
    def list_resources(self) -> List[Dict[str, Any]]:
        """List available resources"""
        return [
            {"id": rid, **data} 
            for rid, data in self.resources.items()
        ]
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get server information"""
        return {
            "name": "Simple Governance MCP Server",
            "version": "1.0.0",
            "protocol_version": "2024-11-05",
            "capabilities": {
                "tools": True,
                "resources": True,
                "prompts": False,
                "logging": False
            },
            "tools_count": len(self.tools),
            "resources_count": len(self.resources)
        }