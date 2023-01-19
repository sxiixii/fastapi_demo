from typing import Any
from uuid import UUID

from aioredis import Redis
from core.config import settings
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError, TransportError
from models.base import orjson_dumps
from models.film import FilmModel as FM
from models.film import RoleAndFilmsModel as RAF
from models.genre import GenreModel as GM
from models.person import PersonModel as PM
from orjson import loads as orjson_loads

from .utils import QueryParameterHandler


class BaseService:
    """
    Базовый класс для всех сервисов
    """

    def __init__(
        self, index: str, model: Any, elastic: AsyncElasticsearch, redis: Redis
    ):
        self.index = index
        self.model = model
        self.elastic = elastic
        self.redis = redis
        self.params_handler = QueryParameterHandler()

    async def get_by_id(self, id: str | UUID) -> FM | GM | PM | None:
        redis_key = self.redis_key(id)
        obj = await self._obj_from_cache(redis_key)
        if not obj:
            try:
                doc = await self.elastic.get(index=self.index, id=id)
            except (NotFoundError, TransportError):
                obj = None
            else:
                obj = self.model(**doc["_source"])
                await self._put_obj_to_cache(redis_key, obj)
        return obj

    async def get_by_params(self, **params) -> list[FM | GM | PM | None]:
        es_query_body = self.params_handler.get_es_query_body(params)
        redis_key = self.redis_key(es_query_body)
        obj_list = await self._list_from_cache(redis_key)
        if not obj_list:
            try:
                doc = await self.elastic.search(body=es_query_body, index=self.index)
            except (NotFoundError, TransportError):
                obj_list = None
            else:
                obj_list = [
                    self.model(**_doc["_source"]) for _doc in doc["hits"]["hits"]
                ]
                await self._put_list_to_cache(redis_key, obj_list)
        return obj_list

    async def get_person_films(self, person: PM) -> list[RAF] | None:
        key = self.redis_key(person.id)
        films = await self._obj_from_cache(key)
        if not films:
            films = await self._get_person_films_from_elastic(person)
            if not films:
                return None
        return films

    async def _get_person_films_from_elastic(self, person: PM) -> list[RAF] | None:
        roles_and_films = person.roles
        ids_list = set()
        for item in roles_and_films:
            ids_list.update(item.film_ids)
        body = {"query": {"terms": {"id": list(ids_list), "boost": 1.0}}}
        try:
            doc = await self.elastic.search(index="movies", body=body)
        except NotFoundError:
            return None
        list_of_films = doc["hits"]["hits"]
        list_of_role_and_films = []
        for item in roles_and_films:
            films_obj = [
                FM(
                    id=film["_source"]["id"],
                    title=film["_source"]["title"],
                    imdb_rating=film["_source"]["imdb_rating"],
                    genre=film["_source"]["genre"],
                )
                for film in list_of_films
                if UUID(film["_source"]["id"]) in item.film_ids
            ]
            list_of_role_and_films.append(RAF(role=item.role, films=films_obj))
        return list_of_role_and_films

    def redis_key(self, key: UUID | dict) -> str:
        return f"{self.index}::{str(key)}"

    async def _obj_from_cache(self, redis_key: str) -> FM | GM | PM | None:
        data = await self.redis.get(redis_key)
        if not data:
            return None
        return self.model.parse_raw(data)

    async def _list_from_cache(self, redis_key: str) -> list[FM | GM | PM] | None:
        data = await self.redis.get(redis_key)
        if not data:
            return None
        return [self.model.parse_raw(_data) for _data in orjson_loads(data)]

    async def _put_obj_to_cache(self, redis_key: str, obj: FM | GM | PM | None):
        await self.redis.set(redis_key, obj.json(), expire=settings.cache_expires)

    async def _put_list_to_cache(
        self, redis_key: str, obj_list: list[FM | GM | PM | None]
    ):
        await self.redis.set(
            redis_key,
            orjson_dumps(obj_list, default=self.model.json),
            expire=settings.cache_expires,
        )
