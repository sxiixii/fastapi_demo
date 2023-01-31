from functools import lru_cache

from core.config import person_settings
from db.base import BaseCache, BaseDB
from db.elastic import get_base_elastic
from db.redis import get_redis
from fastapi import Depends
from models.person import PersonModel
from services.base import BaseService


class PersonService(BaseService):
    pass


@lru_cache()
def get_person_service(
    cache: BaseCache = Depends(get_redis),
    elastic: BaseDB = Depends(get_base_elastic),
) -> PersonService:
    return PersonService(
        index=person_settings.es_index,
        model=PersonModel,
        elastic=elastic,
        cache=cache,
    )
