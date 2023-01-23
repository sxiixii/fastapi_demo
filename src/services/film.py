from functools import lru_cache

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models.film import FilmModel
from services.base import BaseService
from core.config import film_settings


class FilmService(BaseService):
    pass


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(index=film_settings.es_index, model=FilmModel, elastic=elastic, redis=redis)
