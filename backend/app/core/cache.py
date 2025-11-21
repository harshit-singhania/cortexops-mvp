import redis
import json
import hashlib
from typing import Optional, Any
from app.core.config import settings

class CacheService:
    def __init__(self):
        self.redis = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True
        )
        self.ttl = 3600  # 1 hour default TTL

    def _generate_key(self, prefix: str, data: Any) -> str:
        """Generate a unique key based on prefix and data content."""
        data_str = json.dumps(data, sort_keys=True)
        hash_str = hashlib.sha256(data_str.encode()).hexdigest()
        return f"{prefix}:{hash_str}"

    def get(self, prefix: str, key_data: Any) -> Optional[str]:
        key = self._generate_key(prefix, key_data)
        return self.redis.get(key)

    def set(self, prefix: str, key_data: Any, value: str, ttl: int = None):
        key = self._generate_key(prefix, key_data)
        self.redis.set(key, value, ex=ttl or self.ttl)

cache_service = CacheService()
