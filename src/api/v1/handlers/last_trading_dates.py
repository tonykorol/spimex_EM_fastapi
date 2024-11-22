from fastapi import APIRouter, Query, Request
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.cache.cache_services import get_cache, generate_cache_key, set_cache, get_cache_or_cache_key
from src.database.database import get_async_session
from src.schemas.schemas import SpimexLastTradingDatesListSchema
from src.api.v1.services.last_trading_dates import get_last_trading_dates

router = APIRouter(prefix="/last_trading_dates")

@router.get("/", response_model=SpimexLastTradingDatesListSchema)
async def last_trading_dates(
        request: Request,
        count: int = Query(ge=1, default=10),
        session: AsyncSession = Depends(get_async_session),
):
    """
    Get last trading dates
    """
    result, cache_key = await get_cache_or_cache_key(request.method, request.url)
    if result is None:
        result = await get_last_trading_dates(count, session)
        await set_cache(cache_key, result)
    return {"dates": result}
