import elasticsearch.exceptions
from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from orjson import loads as orjson_loads
from core.config import CACHE_EXPIRE_IN_SECONDS
from models.base import orjson_dumps
from models.film import FilmDetailedResponse as FDR
from models.genre import GenreDetailedResponse as GDR
from models.person import PersonDetailedResponse as PDR

from .utils import get_body


class BaseService:
    '''
    Базовый класс для всех сервисных классов, содержащий общую бизнес-логику
    '''
    def __init__(self, index: str, model: FDR | GDR | PDR | None, elastic: AsyncElasticsearch, redis: Redis) -> None:
        self.index = index
        self.model = model
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, id: str) -> FDR | GDR | PDR | None:
        '''
        вернуть объект по идентификатору
        '''
        # cначала попробуем достать из кэша
        redis_key = self.redis_key(id)
        obj = await self._obj_from_cache(redis_key)
        if not obj: # если нет - достаем из эластика
            try:
                doc = await self.elastic.get(index=self.index, id=id)
            except elasticsearch.exceptions.NotFoundError:
                # если нет в эластике - значит нет вообще с таким идентификатором
                obj = None
            else:
                # если нашли - запишем в кэш
                obj = self.model(**doc["_source"])
                await self._put_obj_to_cache(redis_key, obj)
        return obj

    async def get_by_params(self, **params) -> list[FDR | GDR | PDR | None]:
        '''
        вернуть объекты по параметрам
        '''
        body = get_body(**params)
        # cначала попробуем достать из кэша
        redis_key = self.redis_key(body)
        obj_list = await self._list_from_cache(redis_key)
        if not obj_list: # если нет - достаем из эластика
            try:
                doc = await self.elastic.search(body=body, index=self.index)
            except elasticsearch.exceptions.NotFoundError:
                # если нет в эластике - значит нет вообще с таким идентификатором
                obj_list = None
            else:
                # если нашли - запишем в кэш
                obj_list = [self.model(**_doc["_source"]) for _doc in doc["hits"]["hits"]]
                await self._put_list_to_cache(redis_key, obj_list)
        return obj_list

    def redis_key(self, params):
        return hash(self.index + orjson_dumps(params))

    async def _obj_from_cache(self, redis_key: int) -> FDR | GDR | PDR | None:
        '''
        вернуть объект из кэша
        '''
        data = await self.redis.get(redis_key)
        if not data:
            return None
        else:
            return self.model.parse_raw(data)

    async def _list_from_cache(self, redis_key: int) -> list[FDR | GDR | PDR] | None:
        '''
        вернуть несколько объектов из кэша
        '''
        data = await self.redis.get(redis_key)
        if not data:
            return None
        else:
            return [self.model.parse_raw(_data) for _data in orjson_loads(data)]

    async def _put_obj_to_cache(self, redis_key: int, obj: FDR | GDR | PDR | None):
        '''
        положить объект в кэш
        '''
        await self.redis.set(redis_key, obj.json(), expire=CACHE_EXPIRE_IN_SECONDS)

    async def _put_list_to_cache(self, redis_key: int, obj_list: list[FDR | GDR | PDR | None]):
        '''
        положить объекты в кэш
        '''
        await self.redis.set(redis_key,orjson_dumps(obj_list, default=self.model.json),expire=CACHE_EXPIRE_IN_SECONDS)
