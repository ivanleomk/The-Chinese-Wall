from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis
import openai
from settings import get_settings
from lib.redis import reconnect_redis

@asynccontextmanager
async def lifespan(app: FastAPI):
    await reconnect_redis();
    openai.api_key = get_settings().OPENAI_API_KEY
    yield
