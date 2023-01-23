from uuid import uuid4

import pytest

from ..settings import person_settings, film_settings

PERSON_PATH = '/api/v1/persons/'
PERSON_INDEX = person_settings.es_index
MOVIE_INDEX = film_settings.es_index


@pytest.mark.parametrize('query_data, expected_answer', [
    (
            {},
            {'status': 200, 'length': 50}
    ),
    (
            {'query': 'Allison'},
            {'status': 200, 'length': 50}
    ),
    (
            {'query': 'Allispn'},
            {'status': 200, 'length': 50}
    ),
    (
            {'query': 'Don'},
            {'status': 200, 'length': 0}
    ),
    (
            {'query': 1},
            {'status': 200, 'length': 0}
    ),
]
                         )
@pytest.mark.asyncio
async def test_persons_search(
        es_write_data,
        make_get_request,
        person_data,
        query_data: dict,
        expected_answer: dict,
):
    await es_write_data(person_data, PERSON_INDEX)
    path = PERSON_PATH + 'search'
    body, headers, status = await make_get_request(path, query_data)
    assert status == expected_answer.get('status')
    assert len(body) == expected_answer.get('length')


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'id': '0a38f642-a28f-4170-a389-e825be5af770'},
                {'status': 200}
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
async def test_person_films(
        es_write_data,
        make_get_request,
        person_data,
        get_films_data,
        query_data: dict,
        expected_answer: dict,
):
    await es_write_data(person_data, PERSON_INDEX)
    await es_write_data(get_films_data, MOVIE_INDEX)
    path = PERSON_PATH + query_data.get('id') + '/film'
    body, headers, status = await make_get_request(path, query_data)
    assert status == expected_answer.get('status')


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'id': 'f76a362d-4e97-4471-857e-4e43662412c9'},
                {'status': 200}
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
async def test_persons_search_by_id(
        es_write_data,
        make_get_request,
        query_data: dict,
        expected_answer: dict,
):
    person_id = 'f76a362d-4e97-4471-857e-4e43662412c9'
    person_data = [{
        'id': person_id,
        'name': 'Mark',
        'roles': [
            {'role': 'actor', 'film_ids': [str(uuid4())]},

        ]
    }]
    await es_write_data(person_data, PERSON_INDEX)
    path = PERSON_PATH + query_data.get('id')
    body, headers, status = await make_get_request(path, query_data)
    assert status == expected_answer.get('status')


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'page[number]': 1, 'page[size]': 20},
                {'status': 200, 'length': 20}
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
async def test_persons_pagination(
        es_write_data,
        make_get_request,
        person_data,
        query_data: dict,
        expected_answer: dict,
):
    await es_write_data(person_data, PERSON_INDEX)
    path = PERSON_PATH + 'search'
    body, headers, status = await make_get_request(path, query_data)
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
async def test_person_redis(
        es_write_data,
        make_get_request,
        person_data,
        get_redis_keys,
        query_data,
        expected_answer,
):
    before_request_keys = await get_redis_keys(PERSON_INDEX)
    await es_write_data(person_data, PERSON_INDEX)
    path = PERSON_PATH + 'search'
    body, headers, status = await make_get_request(path, query_data)
    after_request_keys = await get_redis_keys(PERSON_INDEX)
    assert status == expected_answer.get('status')
    assert len(before_request_keys) == 0
    assert len(after_request_keys) == expected_answer.get('keys')
