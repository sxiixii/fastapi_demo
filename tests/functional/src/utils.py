import json

from elasticsearch import AsyncElasticsearch

from ..settings import base_settings


async def get_redis_keys(redis_client, index):
    match = index + "*"
    cur = b"0"
    keys = None
    while cur:
        cur, keys = await redis_client.scan(cur, match=match)
    return keys


async def make_get_request(http_session, path, query_data):
    url = base_settings.service_url + path
    async with http_session.get(url, params=query_data) as response:
        body = await response.json()
        headers = response.headers
        status = response.status
        return body, headers, status


def _generate_data(es_data, es_index, es_id_field):
    actions = []
    for row in es_data:
        action = {"index": {"_index": es_index, "_id": row[es_id_field]}}
        doc = json.dumps(row)
        actions.append(action)
        actions.append(doc)
    return actions


async def es_write_data(es_client: AsyncElasticsearch, data: list[dict], index: str):
    bulk_data = _generate_data(data, index, base_settings.es_id_field)
    response = await es_client.bulk(
        operations=bulk_data,
        refresh=True,
    )
    await es_client.close()
    if response["errors"]:
        raise Exception("Ошибка записи данных в Elasticsearch")
