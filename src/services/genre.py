from functools import lru_cache

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models.genre import GenreModel
from services.base import BaseService
from core.config import genre_settings


class GenreService(BaseService):
    pass


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(index=genre_settings.es_index, model=GenreModel, elastic=elastic, redis=redis)
