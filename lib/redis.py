import asyncio
from fastapi import HTTPException
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter

from settings import get_settings
from fastapi_limiter.depends import RateLimiter

rate_limit_middleware = RateLimiter(times=2, seconds=20)


async def reconnect_redis():
    global redis_client
    redis_client = redis.from_url(
        get_settings().REDIS_URL, encoding="utf-8", decode_responses=True
    )
    await FastAPILimiter.init(redis_client)


async def verify_redis_connection(retries=3) -> None:
    for i in range(retries):
        try:
            print("Verifying User Connection")
            r = await redis.from_url(get_settings().REDIS_URL)
            await r.ping()
            print(
                "Verifying that LUA Script is initialised in rate limiter by passing in dummy user"
            )
            await rate_limit_middleware._check("test")
            break
        except Exception as e:
            if i < retries - 1:
                await reconnect_redis()
                continue
            else:
                raise HTTPException(
                    status_code=500, detail="Unable to connect to Redis"
                )
