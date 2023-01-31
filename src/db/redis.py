from typing import Any
from uuid import UUID

from aioredis import Redis
from core.config import settings
from db.base import BaseCache
from models.film import RoleAndFilmsModel
from models.person import PersonModel
from orjson import dumps as orjson_dumps
from orjson import loads as orjson_loads
from pydantic import BaseModel

redis: Redis | None = None


class RedisCache(BaseCache):
    def __init__(self, redis: Redis):
        self.redis = redis

    def transform_to_redis_key(self, key: UUID | str | dict, index: str) -> str:
        return f"{index}::{str(key)}"

    async def get(
        self,
        params: UUID | str | dict,
        index: str,
        model: BaseModel,
    ) -> Any | list[Any]:
        """
        обращается в redis за данными.
        Если нет - вернет None.
        Если есть - вернет модель или список моделей
        """
        key = params
        if isinstance(params, PersonModel):
            key = params.id
        redis_key = self.transform_to_redis_key(key=key, index=index)
        data = await self.redis.get(redis_key)
        if not data:
            return None
        if isinstance(params, (dict, PersonModel)):
            if isinstance(params, PersonModel):
                model = RoleAndFilmsModel
            return [model.parse_raw(_data) for _data in orjson_loads(data)]
        return model.parse_raw(data)

    async def put(
        self,
        params: UUID | str | dict,
        index: str,
        response: Any | list[Any],
        model: BaseModel,
    ):
        key = params
        if isinstance(params, PersonModel):
            key = params.id
        redis_key = self.transform_to_redis_key(key=key, index=index)
        if isinstance(params, (dict, PersonModel)):
            if isinstance(params, PersonModel):
                model = RoleAndFilmsModel
            return await self.redis.set(
                redis_key,
                orjson_dumps(response, default=model.json),
                expire=settings.cache_expires,
            )
        return await self.redis.set(
            redis_key, response.json(), expire=settings.cache_expires
        )


async def get_redis() -> RedisCache:
    return RedisCache(redis)
