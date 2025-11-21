from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.sql import func
from app.db.session import Base

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    repo_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Metadata from manifest
    metadata_json = Column(JSON, default={})

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    level = Column(String, index=True)
    message = Column(Text, nullable=False)
    context = Column(JSON, default={})  # Extra fields like trace_id, span_id
    
    # We might want to store the embedding ID here later if we link 1:1, 
    # but usually embeddings are in Qdrant with a payload pointing back here.
