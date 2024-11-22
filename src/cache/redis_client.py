import logging

import redis.asyncio as redis


class RedisClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.redis = None

    async def connect(self):
        self.redis = await redis.from_url(f"redis://{self.host}:{self.port}")
        logging.info("Connected to redis")

    async def close(self):
        if self.redis:
            await self.redis.close()

    async def clear(self):
        await self.redis.flushdb()

from src.config import REDIS_HOST, REDIS_PORT
redis_client = RedisClient(REDIS_HOST, REDIS_PORT)
