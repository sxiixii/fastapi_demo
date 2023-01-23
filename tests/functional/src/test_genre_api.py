import pytest

from ..settings import genre_settings
from ..testdata.es_data.genre_data import GENRE_CONTROL_UUID

GENRE_PATH = '/api/v1/genres/'
GENRE_INDEX = genre_settings.es_index


@pytest.mark.parametrize('query_data, expected_answer', [
    (
            {},
            {'status': 200, 'length': 9}
    ),
    (
            {'query': 'Sci-Fi'},
            {'status': 200, 'length': 1}
    ),
    (
            {'query': 'Sci'},
            {'status': 200, 'length': 1}
    ),
    (
            {'query': 'Sci-Fo'},
            {'status': 200, 'length': 1}
    ),
    (
            {'query': 'Unbelievable'},
            {'status': 200, 'length': 0}
    ),
    (
            {'query': 1},
            {'status': 200, 'length': 0}
    ),
]
                         )
@pytest.mark.asyncio
async def test_genres_search(
        es_write_data,
        make_get_request,
        get_genres_data,
        query_data: dict,
        expected_answer: dict,
):
    await es_write_data(get_genres_data, GENRE_INDEX)
    body, headers, status = await make_get_request(GENRE_PATH, query_data)
    assert status == expected_answer.get('status')
    assert len(body) == expected_answer.get('length')


@pytest.mark.parametrize('query_data, expected_answer', [
    (
            {'id': GENRE_CONTROL_UUID},
            {'status': 200, 'name': 'Sci-Fi'}
    ),
    (
            {'id': 'f76a362d-4e97-4471-857e-4e43662412c8'},
            {'status': 404}
    ),
    (
            {'id': 'some wrong uuid'},
            {'status': 422}
    ),
]
                         )
@pytest.mark.asyncio
async def test_genres_search_by_id(
        es_write_data,
        make_get_request,
        get_genres_data,
        query_data: dict,
        expected_answer: dict,
):
    await es_write_data(get_genres_data, GENRE_INDEX)
    path = GENRE_PATH + query_data.get('id', '')
    body, headers, status = await make_get_request(path, query_data)
    assert status == expected_answer.get('status')
    assert body.get('name') == expected_answer.get('name')


@pytest.mark.parametrize('query_data, expected_answer', [
    (
            {'page[number]': 1, 'page[size]': 20},
            {'status': 200, 'length': 9}
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
async def test_genres_pagination(
        es_write_data,
        make_get_request,
        get_genres_data,
        query_data: dict,
        expected_answer: dict,
):
    await es_write_data(get_genres_data, GENRE_INDEX)
    body, headers, status = await make_get_request(GENRE_PATH, query_data)
    assert status == expected_answer.get('status')
    assert len(body) == expected_answer.get('length')


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'page[number]': 1, 'page[size]': 20},
                {'status': 200, 'keys': 1}
        ),
    ]
)
@pytest.mark.asyncio
async def test_genre_redis(
        es_write_data,
        make_get_request,
        get_genres_data,
        get_redis_keys,
        query_data,
        expected_answer,
):
    before_request_keys = await get_redis_keys(GENRE_INDEX)
    await es_write_data(get_genres_data, GENRE_INDEX)
    body, headers, status = await make_get_request(GENRE_PATH, query_data)
    after_request_keys = await get_redis_keys(GENRE_INDEX)
    assert status == expected_answer.get('status')
    assert len(before_request_keys) == 0
    assert len(after_request_keys) == expected_answer.get('keys')
