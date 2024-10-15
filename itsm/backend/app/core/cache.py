from app.core.config import settings
from app.core.logging import get_logger
import json
import redis
import diskcache
logger = get_logger(__name__)
class Cache:
    def __init__(self):
        if settings.CACHE_TYPE == "redis":
            self.client = redis.Redis.from_url(settings.REDIS_URL)
        elif settings.CACHE_TYPE == "diskcache":
            self.cache = diskcache.Cache(settings.DISKCACHE_DIR)

    def set(self, key: str, value, expire: int = 300):
        try:
            if settings.CACHE_TYPE == "redis":
                # Serialize the value to JSON
                self.client.setex(key, expire, json.dumps(value))
            elif settings.CACHE_TYPE == "diskcache":
                self.cache.set(key, value, expire=expire)
        except Exception as e:
            logger.error(f"Cache set error: {e}")

    def get(self, key: str):
        try:
            if settings.CACHE_TYPE == "redis":
                # Retrieve and deserialize the JSON value
                value = self.client.get(key)
                if value:
                    return json.loads(value)
                return None
            elif settings.CACHE_TYPE == "diskcache":
                return self.cache.get(key)
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None

    def delete(self, key: str):
        try:
            if settings.CACHE_TYPE == "redis":
                self.client.delete(key)
            elif settings.CACHE_TYPE == "diskcache":
                self.cache.delete(key)
        except Exception as e:
            logger.error(f"Cache delete error: {e}")

