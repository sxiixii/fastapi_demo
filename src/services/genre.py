from functools import lru_cache

from core.config import genre_settings
from db.base import BaseCache, BaseDB
from db.elastic import get_base_elastic
from db.redis import get_redis
from fastapi import Depends
from models.genre import GenreModel
from services.base import BaseService


class GenreService(BaseService):
    pass


@lru_cache()
def get_genre_service(
    cache: BaseCache = Depends(get_redis),
    elastic: BaseDB = Depends(get_base_elastic),
) -> GenreService:
    return GenreService(
        index=genre_settings.es_index,
        model=GenreModel,
        elastic=elastic,
        cache=cache,
    )
