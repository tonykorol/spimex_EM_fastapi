import json
from typing import Optional, List, Union

from src.cache.redis_client import redis_client
from ..models.spimex import SpimexTradingResults


async def get_cache(key)-> Optional[List[dict]]:
    cache = await redis_client.redis.get(key)
    if cache is None:
        return None
    return json.loads(cache)

async def set_cache(key: str, data: List[Union[SpimexTradingResults, dict]]) -> None:
    if data:
        if isinstance(data[0], SpimexTradingResults):
            data = [obj.to_dict() for obj in data]
        await redis_client.redis.set(key, json.dumps(data))

async def clear_cache() -> None:
    if redis_client.redis:
        await redis_client.redis.flushdb()

async def generate_cache_key(method: str, url: str) -> str:
    key = f"{method}:{url}"
    return key

async def get_cache_or_cache_key(method: str, url: str) -> Union[List[dict], str]:
    key = await generate_cache_key(method, url)
    cache = await get_cache(key)
    return cache, key
