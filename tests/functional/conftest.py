import asyncio

import aiohttp
import aioredis
import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch

from .settings import base_settings, film_settings, genre_settings, person_settings


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def es_client():
    client = AsyncElasticsearch(
        hosts=base_settings.es_host,
    )
    yield client
    # удаляем индексы после тестов
    await client.options(ignore_status=[400, 404]).indices.delete(
        index=(
            film_settings.es_index,
            person_settings.es_index,
            genre_settings.es_index,
        ),
        ignore_unavailable=True,
    )
    await client.close()


@pytest_asyncio.fixture
async def redis_client():
    client = await aioredis.create_redis_pool(
        (base_settings.redis_host, base_settings.redis_port),
        minsize=10,
        maxsize=20,
        encoding="utf-8",
    )
    async for key in client.iscan(match="*"):
        await client.delete(key)

    yield client
    client.close()


@pytest_asyncio.fixture(scope="session")
async def http_session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()
