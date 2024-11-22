from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.cache.cache_services import clear_cache
from src.cache.redis_client import redis_client

import logging

async def clear_redis_cache():
    if redis_client.redis:
        await clear_cache()
        logging.info("Redis cache cleared")

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(clear_redis_cache, 'cron', hour=14, minute=11)
    scheduler.start()
    logging.info("Scheduler started")
