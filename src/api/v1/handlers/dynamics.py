from datetime import date, datetime

from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.cache.redis_client import get_redis_client, RedisClient, update_cache_in_background
from src.database.database import get_async_session
from src.api.v1.schemas.schemas import SpimexTradingResultListSchema
from src.api.v1.services.dynamics import get_dynamics

router = APIRouter(prefix='/dynamics')

@router.get('/', response_model=SpimexTradingResultListSchema)
async def dynamics(
        request: Request,
        background_tasks: BackgroundTasks,
        oil_id: str = Query(default=None),
        delivery_type_id: str = Query(default=None),
        delivery_basis_id: str = Query(default=None),
        start_date: date = Query(),
        end_date: date = Query(default=datetime.today().date()),
        session: AsyncSession = Depends(get_async_session),
        redis_client: RedisClient = Depends(get_redis_client),
):
    if start_date >= end_date:
        raise HTTPException(status_code=400, detail="start_date must be less than end_date")

    result, cache_key = await redis_client.get_cache_or_cache_key(request.method, request.url)
    if result is None:
        result = await get_dynamics(
            oil_id,
            delivery_type_id,
            delivery_basis_id,
            session,
            start_date,
            end_date,
        )
        result = {"results": result}

        background_tasks.add_task(update_cache_in_background, redis_client, cache_key, result)
    return result
