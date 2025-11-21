from fastapi import APIRouter
from app.api.endpoints import ingest, query

api_router = APIRouter()
api_router.include_router(ingest.router, prefix="/ingest", tags=["ingestion"])
api_router.include_router(query.router, prefix="/query", tags=["query"])
