from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

if settings.CACHE_TYPE == "redis":
    import redis

    class Cache:
        def __init__(self):
            self.client = redis.Redis.from_url(settings.REDIS_URL)

        def set(self, key: str, value: str, expire: int = 300):
            try:
                self.client.setex(key, expire, value)
            except Exception as e:
                logger.error(f"Redis set error: {e}")

        def get(self, key: str):
            try:
                return self.client.get(key)
            except Exception as e:
                logger.error(f"Redis get error: {e}")
                return None

        def delete(self, key: str):
            try:
                self.client.delete(key)
            except Exception as e:
                logger.error(f"Redis delete error: {e}")

elif settings.CACHE_TYPE == "diskcache":
    import diskcache

    class Cache:
        def __init__(self):
            self.cache = diskcache.Cache(settings.DISKCACHE_DIR)

        def set(self, key: str, value: str, expire: int = 300):
            try:
                self.cache.set(key, value, expire=expire)
            except Exception as e:
                logger.error(f"FileCache set error: {e}")

        def get(self, key: str):
            try:
                return self.cache.get(key)
            except Exception as e:
                logger.error(f"FileCache get error: {e}")
                return None

        def delete(self, key: str):
            try:
                self.cache.delete(key)
            except Exception as e:
                logger.error(f"FileCache delete error: {e}")
