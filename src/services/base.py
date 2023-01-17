import orjson
from aioredis import Redis
from core.config import CACHE_EXPIRE_IN_SECONDS
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError, TransportError
from models.base import orjson_dumps
from models.film import FilmModel as FM
from models.genre import GenreModel as GM
from models.person import PersonModel as PM
from orjson import loads as orjson_loads

from .utils import get_body


class BaseService:
    '''
    Базовый класс для всех сервисных классов, содержащий общую бизнес-логику
    '''
    def __init__(self, index: str, model: FM | GM | PM | None, elastic: AsyncElasticsearch, redis: Redis) -> None:
        self.index = index
        self.model = model
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, id: str) -> FM | GM | PM | None:
        '''
        вернуть объект по идентификатору
        '''
        # cначала попробуем достать из кэша
        redis_key = self.redis_key(id)
        obj = await self._obj_from_cache(redis_key)
        if not obj:  # если нет - достаем из эластика
            try:
                doc = await self.elastic.get(index=self.index, id=id)
            except (NotFoundError, TransportError):
                # если нет в эластике - значит нет вообще с таким идентификатором
                obj = None
            else:
                # если нашли - запишем в кэш
                obj = self.model(**doc["_source"])
                await self._put_obj_to_cache(redis_key, obj)
        return obj

    async def get_by_params(self, **params) -> list[FM | GM | PM | None]:
        '''
        вернуть объекты по параметрам
        '''
        body = get_body(**params)
        # cначала попробуем достать из кэша
        redis_key = self.redis_key(body)
        obj_list = await self._list_from_cache(redis_key)
        if not obj_list:  # если нет - достаем из эластика
            try:
                doc = await self.elastic.search(body=body, index=self.index)
            except (NotFoundError, TransportError):
                # если нет в эластике - значит нет вообще с таким идентификатором
                obj_list = None
            else:
                # если нашли - запишем в кэш
                obj_list = [self.model(**_doc["_source"]) for _doc in doc["hits"]["hits"]]
                await self._put_list_to_cache(redis_key, obj_list)
        return obj_list

    async def get_by_list_of_id(self, ids_list: list[str]) -> list[FM | GM | PM] | None:
        key = self.redis_key(''.join(ids_list))
        films = await self._obj_from_cache(key)
        if not films:
            films = await self._get_by_ids_from_elastic(ids_list)
            if not films:
                return None
        return films

    async def _get_by_ids_from_elastic(self, ids_list: list[str]) -> list[FM | GM | PM] | None:
        body = {'query': {'terms': {'id': ids_list, 'boost': 1.0}}}
        try:
            doc = await self.elastic.search(index='movies', body=body)
        except NotFoundError:
            return None
        list_of_films = doc['hits']['hits']
        return [
            FM(
                id=film['_source']['id'],
                title=film['_source']['title'],
                imdb_rating=film['_source']['imdb_rating'],
                description=film['_source']['description']
            ) for film in list_of_films
        ]

    def redis_key(self, params):
        return hash(self.index + orjson.dumps(params).decode())

    async def _obj_from_cache(self, redis_key: int) -> FM | GM | PM | None:
        '''
        вернуть объект из кэша
        '''
        data = await self.redis.get(redis_key)
        if not data:
            return None
        else:
            return self.model.parse_raw(data)

    async def _list_from_cache(self, redis_key: int) -> list[FM | GM | PM] | None:
        '''
        вернуть несколько объектов из кэша
        '''
        data = await self.redis.get(redis_key)
        if not data:
            return None
        else:
            return [self.model.parse_raw(_data) for _data in orjson_loads(data)]

    async def _put_obj_to_cache(self, redis_key: int, obj: FM | GM | PM | None):
        '''
        положить объект в кэш
        '''
        await self.redis.set(redis_key, obj.json(), expire=CACHE_EXPIRE_IN_SECONDS)

    async def _put_list_to_cache(self, redis_key: int, obj_list: list[FM | GM | PM | None]):
        '''
        положить объекты в кэш
        '''
        await self.redis.set(
            redis_key,
            orjson_dumps(obj_list, default=self.model.json),
            expire=CACHE_EXPIRE_IN_SECONDS
        )
