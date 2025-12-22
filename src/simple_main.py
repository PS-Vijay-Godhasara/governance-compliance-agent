"""Simplified main application"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
from .core.simple_orchestrator import SimpleOrchestrator
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Simple Governance Agent",
    description="Simplified governance and compliance validation",
    version="1.0.0"
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = SimpleOrchestrator()

# Request models
class ValidationRequest(BaseModel):
    policy_id: str
    data: Dict[str, Any]

class KYCRequest(BaseModel):
    customer_data: Dict[str, Any]

class RiskRequest(BaseModel):
    data: Dict[str, Any]


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Simple Governance Agent API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check"""
    return {"status": "healthy"}


@app.get("/policies")
async def list_policies():
    """List available policies"""
    try:
        policies = orchestrator.list_policies()
        return {"policies": policies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/policies/{policy_id}")
async def get_policy(policy_id: str):
    """Get policy details"""
    try:
        policy = orchestrator.get_policy(policy_id)
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        return policy
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/validate")
async def validate_data(request: ValidationRequest):
    """Validate data against policy"""
    try:
        result = orchestrator.validate(request.policy_id, request.data)
        return result
    except Exception as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/kyc")
async def validate_kyc(request: KYCRequest):
    """Perform KYC validation"""
    try:
        result = orchestrator.validate_kyc(request.customer_data)
        return result
    except Exception as e:
        logger.error(f"KYC validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/risk")
async def assess_risk(request: RiskRequest):
    """Assess risk level"""
    try:
        result = orchestrator.assess_risk(request.data)
        return result
    except Exception as e:
        logger.error(f"Risk assessment error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)