from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.cache.redis_client import redis_client


async def clear_redis_cache() -> None:
    if redis_client.redis:
        await redis_client.clear_cache()

def start_scheduler() -> None:
    """
    Запуск планировщика
    """
    scheduler = AsyncIOScheduler()
    scheduler.add_job(clear_redis_cache, 'cron', hour=14, minute=11)
    scheduler.start()
