"""Main application entry point"""

import asyncio
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .core.engine import GovernanceEngine
from .agents.orchestrator import AgentOrchestrator
from .core.logger import setup_logging
from .core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    setup_logging()
    
    # Initialize core components
    engine = GovernanceEngine()
    orchestrator = AgentOrchestrator(engine)
    
    # Store in app state
    app.state.engine = engine
    app.state.orchestrator = orchestrator
    
    yield
    
    # Shutdown
    await engine.shutdown()


# Create FastAPI app
app = FastAPI(
    title="Governance & Compliance Agent",
    description="LLM-powered autonomous governance and compliance validation",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}


@app.post("/policies")
async def register_policy(policy_data: dict):
    """Register a new policy"""
    try:
        orchestrator = app.state.orchestrator
        policy_id = await orchestrator.register_policy(
            name=policy_data["name"],
            content=policy_data["content"],
            metadata=policy_data.get("metadata", {})
        )
        return {"policy_id": policy_id, "status": "registered"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/validate")
async def validate_data(validation_request: dict):
    """Validate data against policies"""
    try:
        orchestrator = app.state.orchestrator
        result = await orchestrator.validate(
            policy_id=validation_request["policy_id"],
            data=validation_request["data"],
            context=validation_request.get("context", {})
        )
        return result.dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/policies/{policy_id}")
async def get_policy(policy_id: str):
    """Get policy details"""
    try:
        orchestrator = app.state.orchestrator
        policy = await orchestrator.get_policy(policy_id)
        return policy.dict()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )