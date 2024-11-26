import hashlib
import json
import logging
from typing import Optional, List, Union

import redis.asyncio as redis

from src.models.spimex import SpimexTradingResults


class RedisClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.redis = None

    async def connect(self):
        try:
            self.redis = await redis.from_url(f"redis://{self.host}:{self.port}")
            await self.redis.ping()
            logging.info("Connected to redis")
        except Exception as e:
            self.redis = None
            logging.error(f"Ошибка при подключении к Redis: {e}")

    async def close(self):
        if self.redis:
            await self.redis.close()

    async def get_cache(self, key) -> Optional[List[dict]]:
        try:
            cache = await self.redis.get(key)
            if cache is None:
                return None
            return json.loads(cache)
        except Exception as e:
            logging.error(f"Ошибка при получении данных из Redis: {e}")

    async def set_cache(self, key: str, data: List[Union[SpimexTradingResults, str]]) -> None:
        try:
            if data:
                await self.redis.set(key, json.dumps(data))
        except Exception as e:
            logging.error(f"Ошибка при установке кэша в Redis: {e}")

    async def clear_cache(self) -> None:
        try:
            if self.redis:
                await self.redis.flushdb()
                logging.info("Cache cleared")
        except Exception as e:
            logging.error(f"Ошибка при очистке Redis: {e}")

    @staticmethod
    async def generate_cache_key(method: str, url: str) -> str:
        key = f"{method}:{url}"
        return hashlib.sha256(key.encode()).hexdigest()

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
