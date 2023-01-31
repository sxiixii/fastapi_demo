from http import HTTPStatus

import pytest

from ..settings import genre_settings
from ..testdata.es_data import GENRE_CONTROL_UUID, genres_data
from .utils import es_write_data, get_redis_keys, make_get_request

GENRE_PATH = "/api/v1/genres/"
GENRE_INDEX = genre_settings.es_index


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({}, {"status": HTTPStatus.OK, "length": 9}),
        ({"query": "Sci-Fi"}, {"status": HTTPStatus.OK, "length": 1}),
        ({"query": "Sci"}, {"status": HTTPStatus.OK, "length": 1}),
        ({"query": "Sci-Fo"}, {"status": HTTPStatus.OK, "length": 1}),
        ({"query": "Unbelievable"}, {"status": HTTPStatus.OK, "length": 0}),
        ({"query": 1}, {"status": HTTPStatus.OK, "length": 0}),
    ],
)
@pytest.mark.asyncio
async def test_genres_search(
    es_client,
    http_session,
    query_data: dict,
    expected_answer: dict,
):
    await es_write_data(es_client, genres_data, GENRE_INDEX)
    body, headers, status = await make_get_request(http_session, GENRE_PATH, query_data)
    assert status == expected_answer.get("status")
    assert len(body) == expected_answer.get("length")


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"id": GENRE_CONTROL_UUID}, {"status": HTTPStatus.OK, "name": "Sci-Fi"}),
        ({"id": "f76a362d-4e97-4471-857e-4e43662412c8"}, {"status": HTTPStatus.NOT_FOUND}),
        ({"id": "some wrong uuid"}, {"status": HTTPStatus.UNPROCESSABLE_ENTITY}),
    ],
)
@pytest.mark.asyncio
async def test_genres_search_by_id(
    es_client,
    http_session,
    query_data: dict,
    expected_answer: dict,
):
    await es_write_data(es_client, genres_data, GENRE_INDEX)
    path = GENRE_PATH + query_data.get("id", "")
    body, headers, status = await make_get_request(http_session, path, query_data)
    assert status == expected_answer.get("status")
    assert body.get("name") == expected_answer.get("name")


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"page[number]": 1, "page[size]": 20}, {"status": HTTPStatus.OK, "length": 9}),
        ({"page[number]": 5000, "page[size]": 300}, {"status": HTTPStatus.OK, "length": 0}),
        (
            {"page[number]": "some", "page[size]": "string"},
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY, "length": 1},
        ),
    ],
)
@pytest.mark.asyncio
async def test_genres_pagination(
    es_client,
    http_session,
    query_data: dict,
    expected_answer: dict,
):
    await es_write_data(es_client, genres_data, GENRE_INDEX)
    body, headers, status = await make_get_request(http_session, GENRE_PATH, query_data)
    assert status == expected_answer.get("status")
    assert len(body) == expected_answer.get("length")


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"page[number]": 1, "page[size]": 20}, {"status": HTTPStatus.OK, "keys": 1}),
    ],
)
@pytest.mark.asyncio
async def test_genre_redis(
    es_client,
    http_session,
    redis_client,
    query_data,
    expected_answer,
):
    before_request_keys = await get_redis_keys(redis_client, GENRE_INDEX)
    await es_write_data(es_client, genres_data, GENRE_INDEX)
    body, headers, status = await make_get_request(http_session, GENRE_PATH, query_data)
    after_request_keys = await get_redis_keys(redis_client, GENRE_INDEX)
    assert status == expected_answer.get("status")
    assert len(before_request_keys) == 0
    assert len(after_request_keys) == expected_answer.get("keys")
