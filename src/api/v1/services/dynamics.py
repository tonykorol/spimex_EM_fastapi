from datetime import date
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.spimex import SpimexTradingResults


async def get_dynamics(
        oil_id: str,
        delivery_type_id: str,
        delivery_basis_id: str,
        session: AsyncSession,
        start_date: date = None,
        end_date: date = None,
) -> List[SpimexTradingResults]:
    """
    Получает список торговых результатов на основе заданных параметров.

    Этот метод выполняет запрос к базе данных для получения торговых результатов
    в указанный период времени и по заданным критериям (идентификаторы нефти,
    типа доставки и базы доставки).
    """
    query = (select(SpimexTradingResults).order_by(SpimexTradingResults.date))

    if start_date and end_date:
        query = query.filter(
            SpimexTradingResults.date >= start_date,
            SpimexTradingResults.date <= end_date, )
    if oil_id:
        query = query.filter(SpimexTradingResults.oil_id == oil_id.upper())
    if delivery_type_id:
        query = query.filter(SpimexTradingResults.delivery_type_id == delivery_type_id.upper())
    if delivery_basis_id:
        query = query.filter(SpimexTradingResults.delivery_basis_id == delivery_basis_id.upper())

    result = await session.execute(query)
    result = result.unique().scalars().all()
    result = [el.to_dict() for el in result]

    return result
