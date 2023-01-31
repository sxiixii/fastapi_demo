from http import HTTPStatus

import pytest

from ..settings import film_settings
from ..testdata.es_data import films_data
from .utils import es_write_data, make_get_request

MOVIE_PATH = "/api/v1/films/"
MOVIE_INDEX = film_settings.es_index


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {},  # ищем без параметров, ожидаем 10 фильмов (10 на страницу)
            {"status": HTTPStatus.OK, "length": 10},
        ),
        (
            {
                "query": "Star"
            },  # ищем с параметром title Star, ожидаем 10, так как все фильмы в индексе The Star
            {"status": HTTPStatus.OK, "length": 10},
        ),
        (
            {
                "query": "Str"
            },  # ищем с опечаткой title Str, ожидаем 10, так как все фильмы в индексе The Star
            {"status": HTTPStatus.OK, "length": 10},
        ),
        (
            {
                "query": "Monty"
            },  # ищем с параметром tittle Monty, ожидаем 0, так как все фильмы в индексе The Star
            {"status": HTTPStatus.OK, "length": 0},
        ),
        (
            {"query": 1},  # ищем с неправильным параметром, ожидаем 0
            {"status": HTTPStatus.OK, "length": 0},
        ),
    ],
)
@pytest.mark.asyncio
async def test_films_search(
    es_client,
    http_session,
    query_data: dict,
    expected_answer: dict,
):
    await es_write_data(es_client, films_data, MOVIE_INDEX)
    path = MOVIE_PATH + "search"
    body, headers, status = await make_get_request(http_session, path, query_data)
    assert status == expected_answer.get("status")
    assert len(body) == expected_answer.get("length")


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {
                "id": "fbf15226-49bc-442a-b3fb-dafa3af8c607"
            },  # uuid есть среди сгенерированных
            {"status": HTTPStatus.OK, "title": "The Star"},
        ),
        (
            {
                "id": "f76a362d-4e97-4471-857e-4e43662412c8"
            },  # uuid нет среди сгенерированных
            {"status": HTTPStatus.NOT_FOUND},
        ),
        ({"id": "some wrong uuid"}, {"status": HTTPStatus.UNPROCESSABLE_ENTITY}),  # вообще не uuid
    ],
)
@pytest.mark.asyncio
async def test_films_search_by_id(
    es_client,
    http_session,
    query_data: dict,
    expected_answer: dict,
):
    await es_write_data(es_client, films_data, MOVIE_INDEX)
    path = MOVIE_PATH + query_data.get("id", "")
    body, headers, status = await make_get_request(http_session, path, query_data)
    assert status == expected_answer.get("status")
    assert body.get("title") == expected_answer.get("title")


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"page[number]": 1, "page[size]": 1}, {"status": HTTPStatus.OK, "length": 1}),
        ({"page[number]": 5000, "page[size]": 300}, {"status": HTTPStatus.OK, "length": 0}),
        (
            {"page[number]": "some", "page[size]": "string"},
            {"status": HTTPStatus.UNPROCESSABLE_ENTITY, "length": 1},
        ),
    ],
)
@pytest.mark.asyncio
async def test_films_pagination(
    es_client,
    http_session,
    query_data: dict,
    expected_answer: dict,
):
    await es_write_data(es_client, films_data, MOVIE_INDEX)
    path = MOVIE_PATH + "search"
    body, headers, status = await make_get_request(http_session, path, query_data)
    assert status == expected_answer.get("status")
    assert len(body) == expected_answer.get("length")
