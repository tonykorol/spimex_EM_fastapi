from datetime import date, datetime

from fastapi import APIRouter, Request, HTTPException
from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.cache.cache_services import generate_cache_key, get_cache, set_cache
from src.database.database import get_async_session
from src.schemas.schemas import SpimexTradingResultListSchema
from src.api.v1.services.dynamics import get_dynamics

router = APIRouter(prefix='/dynamics')

@router.get('/', response_model=SpimexTradingResultListSchema)
async def dynamics(
        request: Request,
        oil_id: str = Query(default=None),
        delivery_type_id: str = Query(default=None),
        delivery_basis_id: str = Query(default=None),
        start_date: date = Query(),
        end_date: date = Query(default=datetime.today().date()),
        session: AsyncSession = Depends(get_async_session)
):
    if start_date >= end_date:
        raise HTTPException(status_code=400, detail="start_date must be less than end_date")

    cache_key = await generate_cache_key(request.method, request.url)
    result = await get_cache(cache_key)
    if result is None:
        result = await get_dynamics(
            oil_id,
            delivery_type_id,
            delivery_basis_id,
            session,
            start_date,
            end_date,
        )
        await set_cache(cache_key, result)
    return {"results": result}
