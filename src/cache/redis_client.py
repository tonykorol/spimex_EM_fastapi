import json
import logging
from typing import Optional, List, Union

import redis.asyncio as redis
from fastapi import Depends

from src.models.spimex import SpimexTradingResults


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

    async def get_cache(self, key) -> Optional[List[dict]]:
        cache = await self.redis.get(key)
        if cache is None:
            return None
        return json.loads(cache)

    async def set_cache(self, key: str, data: List[Union[SpimexTradingResults, str]]) -> None:
        if data:
            # if isinstance(data.get('results')[0], SpimexTradingResults):
            #     data = [obj.to_dict() for obj in data]
            await self.redis.set(key, json.dumps(data))

    async def clear_cache(self) -> None:
        if self.redis:
            await self.redis.flushdb()

    @staticmethod
    async def generate_cache_key(method: str, url: str) -> str:
        return f"{method}:{url}"

    async def get_cache_or_cache_key(self, method: str, url: str) -> Union[List[dict], str]:
        key = await self.generate_cache_key(method, url)
        cache = await self.get_cache(key)
        return cache, key

async def update_cache_in_background(redis_client: RedisClient, key: str, data) -> None:
    await redis_client.set_cache(key, data)

from src.config import REDIS_HOST, REDIS_PORT

redis_client = RedisClient(REDIS_HOST, REDIS_PORT)

async def get_redis_client():
    return redis_client

