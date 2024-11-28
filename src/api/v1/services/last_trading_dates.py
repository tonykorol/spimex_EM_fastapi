from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.schemas.schemas import SpimexLastTradingDatesListSchema
from src.models.spimex import SpimexTradingResults


async def get_last_trading_dates(page: int, size: int, count: int, session: AsyncSession) -> List[SpimexLastTradingDatesListSchema]:
    """
    Получает список последних торговых дат согласно заданному количеству

    Этот метод выполняет запрос к базе данных для получения списка последних торговых дней
    в указанном количестве.
    """
    offset_min = page * size
    offset_max = (page + 1) * size
    stmt = await session.execute(
        select(SpimexTradingResults.date)
        .order_by(SpimexTradingResults.date.desc())
        .distinct()
        .limit(count)
    )
    results = stmt.unique().scalars().all()
    results = [i.date().isoformat() for i in results]
    return results[offset_min:offset_max]
