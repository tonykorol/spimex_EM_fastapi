import asyncio

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config import settings
from src.database.database import Base, get_async_session
from src.main import app
from src.models.spimex import SpimexTradingResults

from tests.fixtures.postgres.spimex_trading_results import TRADING_RESULTS

engine = create_async_engine(settings.DB_URL)
TestAsyncSession = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope='session')
def event_loop(request: pytest.FixtureRequest) -> asyncio.AbstractEventLoop:
    """Returns a new event_loop."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://localhost:8000") as client:
        yield client


@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_test_db(event_loop, get_test_data):
    assert settings.MODE == "TEST"
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestAsyncSession() as session:
        session.add_all(get_test_data)
        await session.commit()

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def get_test_data():
    return [SpimexTradingResults(**_) for _ in TRADING_RESULTS]


@pytest.fixture(scope="session", autouse=True)
async def override_get_db(init_test_db):
    async def _get_async_session():
        async with TestAsyncSession() as session:
            yield session
    app.dependency_overrides[get_async_session] = _get_async_session
