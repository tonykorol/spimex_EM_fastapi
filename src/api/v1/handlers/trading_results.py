from fastapi import APIRouter, Depends, Request, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from src.cache.redis_client import RedisClient, get_redis_client, update_cache_in_background
from src.database.database import get_async_session
from src.api.v1.schemas.schemas import SpimexTradingResultListSchema
from src.api.v1.services.dynamics import get_dynamics

router = APIRouter(prefix="/trading_results")

@router.get("/", response_model=SpimexTradingResultListSchema)
async def trading_results(
        request: Request,
        background_tasks: BackgroundTasks,
        oil_id: str,
        delivery_type_id: str,
        delivery_basis_id: str,
        session: AsyncSession = Depends(get_async_session),
        redis_client: RedisClient = Depends(get_redis_client),
):
    result, cache_key = await redis_client.get_cache_or_cache_key(request.method, request.url)
    if result is None:
        result = await get_dynamics(oil_id, delivery_type_id, delivery_basis_id, session)
        result = {"results": result}
        background_tasks.add_task(update_cache_in_background, redis_client, cache_key, result)
    return result