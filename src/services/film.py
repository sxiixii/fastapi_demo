from functools import lru_cache

from fastapi import Depends

from core.config import film_settings
from db.elastic import get_films_elastic
from db.redis import RedisCache, get_redis
from models.film import FilmModel
from services.base import BaseService


class FilmService(BaseService):
    pass


@lru_cache()
def get_film_service(
        cache: RedisCache = Depends(get_redis),
        elastic=Depends(get_films_elastic),
) -> FilmService:
    return FilmService(index=film_settings.es_index, model=FilmModel, elastic=elastic, cache=cache)
