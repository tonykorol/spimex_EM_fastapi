from typing import Any

import pytest
from httpx import AsyncClient

from tests.fixtures import test_cases


class TestLastTradingDatesHandler:

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ('url', 'params', 'expected_status_code', 'expected_payload', 'expectation'),
        test_cases.PARAMS_TEST_TRADING_DATES_HANDLER,
    )
    async def test_last_trading_dates_get(
            url: str,
            params: dict,
            expected_status_code: int,
            expected_payload: dict,
            expectation: Any,
            test_async_client: AsyncClient,
    ) -> None:
        response = await test_async_client.get(url, params=params)
        assert response.status_code == expected_status_code
        assert response.json() == expected_payload