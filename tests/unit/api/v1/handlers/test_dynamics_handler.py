from typing import Any

import pytest
from httpx import AsyncClient

from tests.fixtures import test_cases


class TestDynamicsHandler:

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ('url', 'params', 'expected_status_code', 'expectation'),
        test_cases.PARAMS_TEST_DYNAMICS_HANDLER,
    )
    async def test_dynamics_get(
            url: str,
            params: dict,
            expected_status_code: int,
            expectation: Any,
            test_async_client: AsyncClient,
    ) -> None:
        response = await test_async_client.get(url, params=params)
        assert response.status_code == expected_status_code
