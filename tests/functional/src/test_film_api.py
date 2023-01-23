import pytest

from ..settings import film_settings

MOVIE_PATH = '/api/v1/films/'
MOVIE_INDEX = film_settings.es_index


@pytest.mark.parametrize('query_data, expected_answer', [
    (
            {},  # ищем без параметров, ожидаем 10 фильмов (10 на страницу)
            {'status': 200, 'length': 10}
    ),
    (
            {'query': 'Star'},  # ищем с параметром title Star, ожидаем 10, так как все фильмы в индексе The Star
            {'status': 200, 'length': 10}
    ),
    (
            {'query': 'Str'},  # ищем с опечаткой title Str, ожидаем 10, так как все фильмы в индексе The Star
            {'status': 200, 'length': 10}
    ),
    (
            {'query': 'Monty'},  # ищем с параметром tittle Monty, ожидаем 0, так как все фильмы в индексе The Star
            {'status': 200, 'length': 0}
    ),
    (
            {'query': 1},  # ищем с неправильным параметром, ожидаем 0
            {'status': 200, 'length': 0}
    ),

])
@pytest.mark.asyncio
async def test_films_search(make_get_request,
                            es_write_data,
                            get_films_data: list[dict],
                            query_data: dict,
                            expected_answer: dict):
    await es_write_data(get_films_data, MOVIE_INDEX)
    path = MOVIE_PATH + 'search'
    body, headers, status = await make_get_request(path, query_data)
    assert status == expected_answer.get('status')
    assert len(body) == expected_answer.get('length')


@pytest.mark.parametrize('query_data, expected_answer', [
    (
            {'id': 'fbf15226-49bc-442a-b3fb-dafa3af8c607'},  # uuid есть среди сгенерированных
            {'status': 200, 'title': 'The Star'}
    ),
    (
            {'id': 'f76a362d-4e97-4471-857e-4e43662412c8'},  # uuid нет среди сгенерированных
            {'status': 404}
    ),
    (
            {'id': 'some wrong uuid'},  # вообще не uuid
            {'status': 422}
    ),
])
@pytest.mark.asyncio
async def test_films_search_by_id(
        es_write_data,
        make_get_request,
        get_films_data,
        query_data: dict,
        expected_answer: dict,
):
    await es_write_data(get_films_data, MOVIE_INDEX)
    path = MOVIE_PATH + query_data.get('id', '')
    body, headers, status = await make_get_request(path, query_data)
    assert status == expected_answer.get('status')
    assert body.get('title') == expected_answer.get('title')


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'page[number]': 1, 'page[size]': 1},
                {'status': 200, 'length': 1}
        ),
        (
                {'page[number]': 5000, 'page[size]': 300},
                {'status': 200, 'length': 0}
        ),
        (
                {'page[number]': 'some', 'page[size]': 'string'},
                {'status': 422, 'length': 1}
        ),
    ]
)
@pytest.mark.asyncio
async def test_films_pagination(
        es_write_data,
        make_get_request,
        get_films_data,
        query_data: dict,
        expected_answer: dict,
):
    await es_write_data(get_films_data, MOVIE_INDEX)
    path = MOVIE_PATH + 'search'
    body, headers, status = await make_get_request(path, query_data)
    assert status == expected_answer.get('status')
    assert len(body) == expected_answer.get('length')
