from typing import Any

from fastapi import Request
from pydantic import BaseModel
from pydantic.types import PositiveInt


class Page(BaseModel):
    size: PositiveInt = 50
    number: PositiveInt = 1


class Filter(BaseModel):
    field: str
    value: str | None


class Should(BaseModel):
    field: str
    value: str


class Body(BaseModel):
    query: dict | None
    sort: str | None
    query_filter: Filter | None
    should: list[Should] | None
    page: Page | None


def _validate_query_params(
    query: dict = None,
    sort: str = None,
    page: dict = None,
    query_filter: dict = None,
    should: list = None,
) -> Body:
    page = page and Page(**page)
    if query_filter is not None:
        field = query_filter["field"]
        value = query_filter["value"]
        query_filter = Filter(field=field, value=value)
    if should is not None:
        should_list = []
        for should_item in should:
            field, value = tuple(should_item.items())[0]
            should_list.append(Should(field=field, value=value))
        should = should_list
    body = Body(
        query=query, sort=sort, query_filter=query_filter, page=page, should=should
    )
    return body


def get_body(**raw_params) -> dict[str, Any]:
    query_body: dict[str, Any] = {}
    params = _validate_query_params(**raw_params)

    # pagination
    if params.page is not None:
        query_body["from"] = (params.page.number - 1) * params.page.size
        query_body["size"] = params.page.size

    # searching
    if params.query is not None and params.query["value"] is not None:
        query_body.setdefault("query", {}).update(_get_search_query(params.query))
    if params.query_filter is not None and params.query_filter.value is not None:
        query_body.setdefault("query", {}).update(
            _get_filter_query(params.query_filter)
        )
    if params.should is not None:
        query_body.setdefault("query", {}).update(_get_should_query(params.should))
    if "query" not in query_body:
        query_body["query"] = {"match_all": {}}

    # sorting
    if params.sort:
        field = params.sort.removeprefix("-")
        direction = "desc" if params.sort.startswith("-") else "asc"
        query_body["sort"] = {field: {"order": direction}}

    return query_body


def _get_search_query(query: dict) -> dict:
    value = query["value"]
    return {
        "fuzzy": {
            query["field"]: {
                "value": value.lower(),
                "fuzziness": "AUTO",
                "max_expansions": 50,
                "prefix_length": 0,
                "transpositions": "true",
                "rewrite": "constant_score",
            }
        }
    }


def _get_filter_query(_filter: Filter) -> dict:
    return {"match": {_filter.field: {"query": _filter.value}}}


def _get_should_query(should_list: list[Should]) -> dict:
    # selected items by id in list
    return {
        "bool": {
            "should": [
                {"match": {should.field: should.value}} for should in should_list
            ]
        }
    }


def get_params(request: Request) -> dict[str, str | dict]:
    params: dict[str, str | dict] = {}
    for key, value in request.query_params.items():
        nested_key = key.removesuffix("]").split("[")
        if len(nested_key) == 2:
            params.setdefault(nested_key[0], {}).update({nested_key[1]: value})
            continue
        params[key] = value

    return params
