from functools import lru_cache

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models.person import PersonModel
from services.base import BaseService
from core.config import person_settings


class PersonService(BaseService):
    pass


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(
        index=person_settings.es_index, model=PersonModel, elastic=elastic, redis=redis
    )
