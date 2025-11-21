from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class LogIngest(BaseModel):
    service_name: str
    timestamp: Optional[datetime] = None
    level: str
    message: str
    context: Optional[Dict[str, Any]] = {}

class ServiceManifestIngest(BaseModel):
    name: str
    description: Optional[str] = None
    repo_url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}

class IngestResponse(BaseModel):
    status: str
    processed_count: int
