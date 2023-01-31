from functools import lru_cache

from fastapi import Depends

from core.config import genre_settings
from db.elastic import get_base_elastic
from db.redis import RedisCache, get_redis
from models.genre import GenreModel
from services.base import BaseService


class GenreService(BaseService):
    pass


@lru_cache()
def get_genre_service(
        cache: RedisCache = Depends(get_redis),
        elastic=Depends(get_base_elastic),
) -> GenreService:
    return GenreService(index=genre_settings.es_index, model=GenreModel, elastic=elastic, cache=cache)
