from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis
import openai
from settings import get_settings
from transformers import pipeline


@asynccontextmanager
async def lifespan(app: FastAPI):
    r = redis.from_url(
        get_settings().REDIS_URL, encoding="utf-8", decode_responses=True
    )
    await FastAPILimiter.init(r)
    openai.api_key = get_settings().OPENAI_API_KEY
    app.pipeline = pipeline(
        "text-classification", model="ivanleomk/bert_password_sniffer"
    )
    yield
