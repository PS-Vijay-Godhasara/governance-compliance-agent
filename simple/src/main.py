"""Simple FastAPI Server for Governance Agent"""

from fastapi import FastAPI, HTTPException
from dataclasses import dataclass
from typing import Dict, Any, List
import os
import sys

# Add src to path
sys.path.append(os.path.dirname(__file__))

from orchestrator import SimpleOrchestrator

app = FastAPI(title="Simple Governance Agent", version="1.0.0")

# Initialize orchestrator
orchestrator = SimpleOrchestrator(use_llm=True)

@dataclass
class ValidationRequest:
    policy_id: str
    data: Dict[str, Any]

@dataclass
class PolicyCreationRequest:
    policy_text: str
    policy_id: str

@dataclass
class KYCRequest:
    identity_documents: List[Dict[str, Any]]
    date_of_birth: str = ""
    address_proof: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.address_proof is None:
            self.address_proof = {}

@dataclass
class RiskRequest:
    amount: float = 0
    country: str = ""
    age: int = 25
    transaction_type: str = ""

@app.get("/")
def root():
    return {"message": "Simple Governance Agent API", "version": "1.0.0"}

@app.post("/validate")
def validate_data(request: dict):
    """Validate data against policy"""
    try:
        policy_id = request.get("policy_id")
        data = request.get("data")
        if not policy_id or not data:
            raise HTTPException(status_code=400, detail="Missing policy_id or data")
        
        result = orchestrator.validate(policy_id, data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/kyc/validate")
def validate_kyc(request: dict):
    """Validate KYC data"""
    try:
        result = orchestrator.validate_kyc(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/risk/assess")
def assess_risk(request: dict):
    """Assess risk factors"""
    try:
        result = orchestrator.assess_risk(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/policies/create")
def create_policy(request: dict):
    """Create policy from natural language"""
    try:
        policy_text = request.get("policy_text")
        policy_id = request.get("policy_id")
        if not policy_text or not policy_id:
            raise HTTPException(status_code=400, detail="Missing policy_text or policy_id")
        
        result = orchestrator.create_policy(policy_text, policy_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/policies")
def list_policies():
    """List available policies"""
    return {"policies": orchestrator.list_policies()}

@app.get("/knowledge/search")
def search_knowledge(query: str, topic: str = None):
    """Search knowledge base"""
    try:
        results = orchestrator.search_knowledge(query, topic)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/mcp/tools")
def list_mcp_tools():
    """List available MCP tools"""
    return {"tools": orchestrator.list_mcp_tools()}

@app.post("/mcp/call")
def call_mcp_tool(request: dict):
    """Call MCP tool"""
    try:
        tool_name = request.get("tool_name")
        parameters = request.get("parameters", {})
        result = orchestrator.call_mcp_tool(tool_name, parameters)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)