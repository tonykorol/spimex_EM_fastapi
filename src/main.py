import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.cache.redis_client import redis_client
from src.api.v1.handlers.last_trading_dates import router as ltd_router
from src.api.v1.handlers.dynamics import router as dyn_router
from src.api.v1.handlers.trading_results import router as tr_router
from src.logging_config import setup_logging
from src.tasks.scheduler import start_scheduler

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Application start")
    await redis_client.connect()
    start_scheduler()
    yield
    await redis_client.clear_cache()
    await redis_client.close()
    logging.info("Application stop")

app = FastAPI(lifespan=lifespan)

app.include_router(ltd_router, tags=["Last Trading Dates"])
app.include_router(dyn_router, tags=["Dynamics"])
app.include_router(tr_router, tags=["Trading Results"])
