"""Simple FastAPI Server for Governance Agent"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import os
import sys

# Add src to path
sys.path.append(os.path.dirname(__file__))

from orchestrator import SimpleOrchestrator

app = FastAPI(title="Simple Governance Agent", version="1.0.0")

# Initialize orchestrator
orchestrator = SimpleOrchestrator(use_llm=True)

class ValidationRequest(BaseModel):
    policy_id: str
    data: Dict[str, Any]

class PolicyCreationRequest(BaseModel):
    policy_text: str
    policy_id: str

class KYCRequest(BaseModel):
    identity_documents: List[Dict[str, Any]] = []
    date_of_birth: str = ""
    address_proof: Dict[str, Any] = {}

class RiskRequest(BaseModel):
    amount: float = 0
    country: str = ""
    age: int = 25
    transaction_type: str = ""

@app.get("/")
def root():
    return {"message": "Simple Governance Agent API", "version": "1.0.0"}

@app.post("/validate")
def validate_data(request: ValidationRequest):
    """Validate data against policy"""
    try:
        result = orchestrator.validate(request.policy_id, request.data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/kyc/validate")
def validate_kyc(request: KYCRequest):
    """Validate KYC data"""
    try:
        data = request.dict()
        result = orchestrator.validate_kyc(data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/risk/assess")
def assess_risk(request: RiskRequest):
    """Assess risk factors"""
    try:
        data = request.dict()
        result = orchestrator.assess_risk(data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/policies/create")
def create_policy(request: PolicyCreationRequest):
    """Create policy from natural language"""
    try:
        result = orchestrator.create_policy(request.policy_text, request.policy_id)
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