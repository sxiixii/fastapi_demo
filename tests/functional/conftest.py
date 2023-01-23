import pytest
import json
import aiohttp
import aioredis
import asyncio

from elasticsearch import AsyncElasticsearch

from .testdata.es_data.film_data import films_data
from .testdata.es_data.person_data import person_main_data
from .testdata.es_data.genre_data import genres_data
from .settings import base_settings, film_settings, genre_settings, person_settings


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def es_client():
    client = AsyncElasticsearch(
        hosts=base_settings.es_host,
    )
    yield client
    # удаляем индексы после тестов
    await client.options(
        ignore_status=[400, 404]).indices.delete(
        index=(film_settings.es_index,
               person_settings.es_index,
               genre_settings.es_index),
        ignore_unavailable=True,
    )
    await client.close()


@pytest.fixture
async def redis_client():
    client = await aioredis.create_redis_pool(
        (base_settings.redis_host, base_settings.redis_port),
        minsize=10,
        maxsize=20,
        encoding='utf-8',
    )
    async for key in client.iscan(match='*'):
        await client.delete(key)

    yield client
    client.close()


@pytest.fixture
def get_redis_keys(redis_client):
    async def inner(index):
        match = index + '*'
        cur = b'0'
        keys = None
        while cur:
            cur, keys = await redis_client.scan(cur, match=match)
        return keys
    return inner


def get_es_bulk_query(es_data, es_index, es_id_field):
    bulk_query = []
    for row in es_data:
        bulk_query.extend([
            json.dumps({'index': {'_index': es_index, '_id': row[es_id_field]}}),
            json.dumps(row)
        ])
    return bulk_query


@pytest.fixture
def es_write_data(es_client: AsyncElasticsearch):
    async def inner(data: list[dict], index: str):
        bulk_query = get_es_bulk_query(data, index, base_settings.es_id_field)
        str_query = '\n'.join(bulk_query) + '\n'
        response = await es_client.bulk(body=str_query, refresh=True)
        await es_client.close()
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


@pytest.fixture(scope="session")
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(session, es_client):
    async def inner(path, query_data):
        url = base_settings.service_url + path
        async with session.get(url, params=query_data) as response:
            body = await response.json()
            headers = response.headers
            status = response.status
            return body, headers, status
    return inner


@pytest.fixture
def person_data():
    return person_main_data


@pytest.fixture
def get_films_data():
    return films_data


@pytest.fixture
def get_genres_data():
    return genres_data
