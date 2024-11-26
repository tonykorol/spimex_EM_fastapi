from fastapi import APIRouter, Query, Request, BackgroundTasks
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.cache.redis_client import RedisClient, get_redis_client, \
    update_cache_in_background
from src.database.database import get_async_session
from src.api.v1.schemas.schemas import SpimexLastTradingDatesListSchema
from src.api.v1.services.last_trading_dates import get_last_trading_dates

router = APIRouter(prefix="/last_trading_dates")

@router.get("/", response_model=SpimexLastTradingDatesListSchema)
async def last_trading_dates(
        request: Request,
        background_tasks: BackgroundTasks,
        count: int = Query(ge=1, default=10),
        session: AsyncSession = Depends(get_async_session),
        redis_client: RedisClient = Depends(get_redis_client),
):
    """
    Get last trading dates
    """
    result, cache_key = await redis_client.get_cache_or_cache_key(request.method, request.url)
    if result is None:
        result = await get_last_trading_dates(count, session)
        result = {"dates": result}
        background_tasks.add_task(update_cache_in_background, redis_client, cache_key, result)
    return result
