from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.db.models import Service, Log
from app.schemas.ingest import LogIngest, ServiceManifestIngest, IngestResponse

router = APIRouter()

@router.post("/manifest", response_model=IngestResponse)
async def ingest_manifest(
    manifest: ServiceManifestIngest,
    db: AsyncSession = Depends(get_db)
):
    # Check if service exists
    result = await db.execute(select(Service).where(Service.name == manifest.name))
    service = result.scalars().first()
    
    if not service:
        service = Service(
            name=manifest.name,
            description=manifest.description,
            repo_url=manifest.repo_url,
            metadata_json=manifest.metadata
        )
        db.add(service)
    else:
        service.description = manifest.description
        service.repo_url = manifest.repo_url
        service.metadata_json = manifest.metadata
    
    await db.commit()
    return IngestResponse(status="success", processed_count=1)

@router.post("/logs", response_model=IngestResponse)
async def ingest_logs(
    logs: List[LogIngest],
    db: AsyncSession = Depends(get_db)
):
    count = 0
    for log_entry in logs:
        # Find service ID (assuming service exists, or create default?)
        # For MVP, we require service to exist or we fail/skip. 
        # Let's try to find it, if not found, maybe create a "unknown" service or error.
        # To be safe and fast, let's assume the service name must match a known service.
        
        result = await db.execute(select(Service).where(Service.name == log_entry.service_name))
        service = result.scalars().first()
        
        if not service:
            # Auto-create service if not exists for smoother ingestion?
            service = Service(name=log_entry.service_name, description="Auto-created from logs")
            db.add(service)
            await db.flush() # get ID
            
        log = Log(
            service_id=service.id,
            timestamp=log_entry.timestamp,
            level=log_entry.level,
            message=log_entry.message,
            context=log_entry.context
        )
        db.add(log)
        
        # Generate and store embedding (async/background task would be better for perf, but inline for MVP)
        # We construct a text representation of the log
        log_text = f"Service: {log_entry.service_name}\nLevel: {log_entry.level}\nMessage: {log_entry.message}\nContext: {log_entry.context}"
        metadata = {
            "service_name": log_entry.service_name,
            "level": log_entry.level,
            "timestamp": str(log_entry.timestamp) if log_entry.timestamp else None,
            "type": "log"
        }
        
        # We need to handle the case where OPENAI_API_KEY is not set
        try:
            from app.services.embeddings import embedding_service
            await embedding_service.ingest_text(log_text, metadata)
        except Exception as e:
            print(f"Warning: Failed to generate embedding: {e}")

        count += 1
        
    await db.commit()
    return IngestResponse(status="success", processed_count=count)
