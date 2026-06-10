import json
from typing import Any

import redis.asyncio as redis

from coding_assistant.config import get_settings

_client: redis.Redis | None = None

RUN_STATE_PREFIX = "run:state:"
RUN_STATE_TTL_SECONDS = 86400


async def get_redis() -> redis.Redis:
    global _client
    if _client is None:
        settings = get_settings()
        _client = redis.from_url(settings.redis_url, decode_responses=True)
    return _client


async def cache_run_state(run_id: str, state: dict[str, Any]) -> None:
    client = await get_redis()
    await client.setex(
        f"{RUN_STATE_PREFIX}{run_id}",
        RUN_STATE_TTL_SECONDS,
        json.dumps(state, default=str),
    )


async def get_cached_run_state(run_id: str) -> dict[str, Any] | None:
    client = await get_redis()
    raw = await client.get(f"{RUN_STATE_PREFIX}{run_id}")
    if raw is None:
        return None
    return json.loads(raw)


async def delete_cached_run_state(run_id: str) -> None:
    client = await get_redis()
    await client.delete(f"{RUN_STATE_PREFIX}{run_id}")
