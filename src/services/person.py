from functools import lru_cache

from fastapi import Depends

from core.config import person_settings
from db.elastic import get_base_elastic
from db.redis import RedisCache, get_redis
from models.person import PersonModel
from services.base import BaseService


class PersonService(BaseService):
    pass


@lru_cache()
def get_person_service(
        cache: RedisCache = Depends(get_redis),
        elastic=Depends(get_base_elastic),
) -> PersonService:
    return PersonService(index=person_settings.es_index, model=PersonModel, elastic=elastic, cache=cache)
