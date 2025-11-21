from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any

from app.agents.reasoning import reasoning_agent
from app.agents.debugger import debugger_agent
from app.agents.docs import docs_agent

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

class RootCauseRequest(BaseModel):
    log_data: str
    context: Optional[str] = ""

class DocsRequest(BaseModel):
    service_name: str
    description: str
    metadata: Dict[str, Any] = {}

@router.post("/chat")
async def chat(request: QueryRequest):
    """
    General system reasoning agent.
    """
    try:
        response = await reasoning_agent.run(request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/rootcause")
async def root_cause(request: RootCauseRequest):
    """
    Log debugger agent for root cause analysis.
    """
    try:
        response = await debugger_agent.analyze(request.log_data, request.context)
        return {"analysis": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/docs/generate")
async def generate_docs(request: DocsRequest):
    """
    Documentation generator agent.
    """
    try:
        response = await docs_agent.generate_docs(
            request.service_name, 
            request.description, 
            request.metadata
        )
        return {"documentation": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
