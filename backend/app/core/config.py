from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "CortexOps"
    API_V1_STR: str = "/api/v1"
    
    # Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    # Vector DB
    QDRANT_HOST: str
    QDRANT_PORT: int = 6333

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int = 6379

    # OpenAI
    OPENAI_API_KEY: Optional[str] = None

    def __init__(self, **data):
        super().__init__(**data)
        if not self.SQLALCHEMY_DATABASE_URI:
            self.SQLALCHEMY_DATABASE_URI = f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
