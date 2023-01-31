from functools import lru_cache

from core.config import film_settings
from db.base import BaseCache, BaseDB
from db.elastic import get_films_elastic
from db.redis import get_redis
from fastapi import Depends
from models.film import FilmModel
from services.base import BaseService


class FilmService(BaseService):
    pass


@lru_cache()
def get_film_service(
    cache: BaseCache = Depends(get_redis),
    elastic: BaseDB = Depends(get_films_elastic),
) -> FilmService:
    return FilmService(
        index=film_settings.es_index,
        model=FilmModel,
        elastic=elastic,
        cache=cache,
    )
