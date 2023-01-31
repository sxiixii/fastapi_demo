import logging
from uuid import UUID

from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import BadRequestError, NotFoundError, TransportError
from models.film import FilmModel, RoleAndFilmsModel
from models.person import PersonModel
from pydantic import BaseModel

from .base import BaseDB
from .utils import QueryParameterHandler

es: AsyncElasticsearch | None = None

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
loggingStreamHandler = logging.StreamHandler()


class ElasticBase(BaseDB):
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic
        self.query_handler = QueryParameterHandler()

    async def get(self, index, model, params) -> BaseModel | None:
        if isinstance(params, dict):
            return await self._search_by_params(index, model, params)
        return await self._get_by_id(index, model, params)

    async def _get_by_id(self, index, model, id) -> BaseModel | None:
        obj = None
        try:
            doc = await self.elastic.get(index=index, id=id)
        except (NotFoundError, TransportError, BadRequestError) as e:
            logger.error("ОШИБКА")
            logger.error(e)
        else:
            obj = model(**doc["_source"])
        return obj

    async def _search_by_params(self, index, model, query_body) -> BaseModel | None:
        valid_query_body = self.query_handler.get_es_query_body(query_body)
        obj_list = None
        try:
            doc = await self.elastic.search(body=valid_query_body, index=index)
        except (NotFoundError, TransportError, BadRequestError) as e:
            logger.error("ОШИБКА")
            logger.error(e)
        else:
            obj_list = [model(**_doc["_source"]) for _doc in doc["hits"]["hits"]]
        return obj_list


class ElasticMovies(ElasticBase):
    async def get(self, index, model, params) -> BaseModel | None:
        if isinstance(params, PersonModel):
            return await self._search_person_films(params)
        return await super().get(index, model, params)

    async def _search_person_films(self, person):

        roles_and_films = person.roles
        ids_list = set()
        for item in roles_and_films:
            ids_list.update(item.film_ids)
        body = {"query": {"terms": {"id": list(ids_list), "boost": 1.0}}}
        try:
            doc = await self.elastic.search(index="movies", body=body)
        except NotFoundError as e:
            logger.error("ОШИБКА")
            logger.error(e)
            return None
        list_of_films = doc["hits"]["hits"]
        list_of_role_and_films = []
        for item in roles_and_films:
            films_obj = [
                FilmModel(
                    id=film["_source"]["id"],
                    title=film["_source"]["title"],
                    imdb_rating=film["_source"]["imdb_rating"],
                    genre=film["_source"]["genre"],
                )
                for film in list_of_films
                if UUID(film["_source"]["id"]) in item.film_ids
            ]
            list_of_role_and_films.append(RoleAndFilmsModel(role=item.role, films=films_obj))
        return list_of_role_and_films


async def get_base_elastic() -> ElasticBase:
    return ElasticBase(elastic=es)


async def get_films_elastic() -> ElasticMovies:
    return ElasticMovies(elastic=es)
