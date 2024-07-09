import redis.asyncio as redis
from app.core.config import settings, logger

class RedisClient:
    redis = None
    url = ''
    soket_timeout = 0

    def __init__(self, url, socket_timeout):
        self.url = url
        self.soket_timeout = socket_timeout

    async def connect_redis(self):
        self.redis = redis.from_url(url=self.url, socket_timeout=self.soket_timeout)

    # Function to disconnect from Redis
    async def disconnect_redis(self):
        if self.redis:
            await self.redis.close()
            logger.info("Disconnected from Redis")


redis_client = RedisClient(settings.REDIS_DATABASE_URL, 5)



