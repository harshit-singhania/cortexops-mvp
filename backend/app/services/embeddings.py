from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.http import models
from app.core.config import settings
import uuid

class EmbeddingService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.client = QdrantClient(
            host=settings.QDRANT_HOST, 
            port=settings.QDRANT_PORT
        )
        self.collection_name = "cortexops_vectors"
        self._ensure_collection()

    def _ensure_collection(self):
        try:
            self.client.get_collection(self.collection_name)
        except Exception:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=1536,  # OpenAI embedding size
                    distance=models.Distance.COSINE
                )
            )

    async def ingest_text(self, text: str, metadata: dict):
        # We use LangChain's Qdrant wrapper for convenience, or direct client
        # For now, let's use the direct client for control or LangChain for ease.
        # Let's use LangChain's wrapper to add texts.
        
        vector_store = Qdrant(
            client=self.client,
            collection_name=self.collection_name,
            embeddings=self.embeddings,
        )
        
        # Add text
        vector_store.add_texts(
            texts=[text],
            metadatas=[metadata]
        )

embedding_service = EmbeddingService()
