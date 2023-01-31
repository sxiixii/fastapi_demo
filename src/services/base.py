import logging
from typing import Any
from uuid import UUID
from pydantic import BaseModel

from db.elastic import ElasticBase
from db.redis import RedisCache

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
loggingStreamHandler = logging.StreamHandler()


class BaseService:
    """
    Базовый класс для всех сервисов
    """
    def __init__(
            self, index: str, model: Any, elastic: ElasticBase, cache: RedisCache):
        self.index = index
        self.model = model
        self.elastic = elastic
        self.cache = cache

    async def get(self, params: dict | UUID | BaseModel) -> BaseModel | list[BaseModel]:
        cached_data = await self.cache.get(
            index=self.index,
            model=self.model,
            params=params,
        )
        if not cached_data:
            model_instance = await self.elastic.get(index=self.index,
                                                    model=self.model,
                                                    params=params)
            if model_instance:
                await self.cache.put(index=self.index,
                                     response=model_instance,
                                     model=self.model,
                                     params=params)
            return model_instance
        return cached_data
