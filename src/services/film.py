from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import FilmDetailedResponse
from services.base import BaseService


class FilmService(BaseService):
    pass


@lru_cache()
def get_film_service(redis: Redis = Depends(get_redis),
                     elastic: AsyncElasticsearch = Depends(get_elastic),) -> FilmService:
    return FilmService(index="movies", model=FilmDetailedResponse, elastic=elastic, redis=redis)
