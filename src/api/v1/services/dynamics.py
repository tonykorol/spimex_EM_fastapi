from datetime import date, datetime
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.spimex import SpimexTradingResults
import logging

# Включаем логирование для SQLAlchemy
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


async def get_dynamics(
        oil_id: str,
        delivery_type_id: str,
        delivery_basis_id: str,
        session: AsyncSession,
        start_date: date = datetime.today().date(),
        end_date: date = datetime.today().date(),
) -> List[SpimexTradingResults]:

    query = (select(SpimexTradingResults)
             .filter(
                    SpimexTradingResults.date >= start_date,
                    SpimexTradingResults.date <= end_date,)
             .order_by(SpimexTradingResults.date))

    if oil_id:
        query = query.filter(SpimexTradingResults.oil_id == oil_id.upper())
    if delivery_type_id:
        query = query.filter(SpimexTradingResults.delivery_type_id == delivery_type_id.upper())
    if delivery_basis_id:
        query = query.filter(SpimexTradingResults.delivery_basis_id == delivery_basis_id.upper())


    # stmt = await session.execute(
    #     select(SpimexTradingResults)
    #     .order_by(SpimexTradingResults.date)
    #     .filter(
    #         SpimexTradingResults.date >= start_date,
    #         SpimexTradingResults.date <= end_date,
    #         SpimexTradingResults.oil_id == oil_id.upper() if oil_id else oil_id,
    #         SpimexTradingResults.delivery_type_id == delivery_type_id.upper() if delivery_type_id else delivery_type_id,
    #         SpimexTradingResults.delivery_basis_id == delivery_basis_id.upper() if delivery_basis_id else delivery_basis_id,
    #     )
    #     .order_by(SpimexTradingResults.date)
    # )
    result = await session.execute(query)
    result = result.unique().scalars().all()

    return result


#
# SELECT spimex_trading_result.id, spimex_trading_result.exchange_product_id, spimex_trading_result.exchange_product_name, spimex_trading_result.oil_id, spimex_trading_result.delivery_basis_id, spimex_trading_result.delivery_basis_name, spimex_trading_result.delivery_type_id, spimex_trading_result.volume, spimex_trading_result.total, spimex_trading_result.count, spimex_trading_result.date, spimex_trading_result.created_on, spimex_trading_result.updated_on
# FROM spimex_trading_result
# WHERE spimex_trading_result.date >= $1::DATE AND spimex_trading_result.date <= $2::DATE AND NULL AND NULL AND NULL ORDER BY spimex_trading_result.date, spimex_trading_result.date
