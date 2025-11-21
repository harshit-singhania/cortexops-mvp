from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.http import models
from app.core.config import settings
import uuid

from typing import List
import numpy as np

class FastEmbedEmbeddingsWrapper(FastEmbedEmbeddings):
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = super().embed_documents(texts)
        return [e.tolist() if isinstance(e, np.ndarray) else e for e in embeddings]

    def embed_query(self, text: str) -> List[float]:
        # Override parent method to avoid "numpy.ndarray is not an iterator" error
        # The parent method calls next() on the result of query_embed, which fails if it returns an array
        res = self._model.query_embed(text)
        
        # Handle generator vs array
        if hasattr(res, '__next__') or hasattr(res, '__iter__') and not isinstance(res, (np.ndarray, list)):
            try:
                embedding = next(res)
            except StopIteration:
                raise ValueError("No embedding generated")
        else:
            embedding = res

        # If we got a list/array of embeddings (e.g. shape [1, D]), take the first one
        if isinstance(embedding, (list, np.ndarray)) and len(embedding) == 1 and isinstance(embedding[0], (list, np.ndarray)):
             embedding = embedding[0]
             
        return embedding.tolist() if isinstance(embedding, np.ndarray) else embedding

class EmbeddingService:
    def __init__(self):
        self.embeddings = FastEmbedEmbeddingsWrapper(model_name="BAAI/bge-small-en-v1.5")
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
                    size=384,  # FastEmbed BGE-small size
                    distance=models.Distance.COSINE
                )
            )

    def get_vector_store(self):
        return Qdrant(
            client=self.client,
            collection_name=self.collection_name,
            embeddings=self.embeddings,
        )

    async def ingest_text(self, text: str, metadata: dict):
        # We use LangChain's Qdrant wrapper for convenience, or direct client
        # For now, let's use the direct client for control or LangChain for ease.
        # Let's use LangChain's wrapper to add texts.
        
        vector_store = self.get_vector_store()
        
        # Add text
        vector_store.add_texts(
            texts=[text],
            metadatas=[metadata]
        )

embedding_service = EmbeddingService()
