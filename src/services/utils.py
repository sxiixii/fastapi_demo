from typing import Any, Optional, Union

from fastapi import Request
from pydantic.types import PositiveInt

from models.base import BaseOrjsonModel


class Page(BaseOrjsonModel):
    size: PositiveInt = 50
    number: PositiveInt = 1


class Filter(BaseOrjsonModel):
    field: str
    value: str


class Should(BaseOrjsonModel):
    field: str
    value: str


class Body(BaseOrjsonModel):
    query: Optional[str]
    sort: Optional[str]
    filter: Optional[Filter]
    should: Optional[list[Should]]
    page: Optional[Page]


def _validate_query_params(
    query: str = None,
    sort: str = None,
    page: dict = None,
    filter: dict = None,
    should: list = None,
) -> Body:
    page = page and Page(**page)
    if filter is not None:
        field, value = tuple(filter.items())[0]
        filter = Filter(field=field, value=value)
    if should is not None:
        should_list = []
        for should_item in should:
            field, value = tuple(should_item.items())[0]
            should_list.append(Should(field=field, value=value))
        should = should_list
    body = Body(query=query, sort=sort, filter=filter, page=page, should=should)
    return body


def get_body(**raw_params) -> dict[str, Any]:
    query_body: dict[str, Any] = {}
    params = _validate_query_params(**raw_params)

    # pagination
    if params.page is not None:
        query_body["from"] = (params.page.number - 1) * params.page.size
        query_body["size"] = params.page.size

    # searching
    if params.query is not None:
        query_body.setdefault("query", {}).update(_get_search_query(params.query))
    if params.filter is not None:
        query_body.setdefault("query", {}).update(_get_filter_query(params.filter))
    if params.should is not None:
        query_body.setdefault("query", {}).update(_get_should_query(params.should))
    if "query" not in query_body:
        query_body["query"] = {"match_all": {}}

    # sorting
    if params.sort is not None:
        field = params.sort.removeprefix("-")
        direction = "desc" if params.sort.startswith("-") else "asc"
        query_body["sort"] = {field: {"order": direction}}

    return query_body


def _get_search_query(query: str) -> dict:
    return {"query_string": {"query": query}}


def _get_filter_query(filter: Filter) -> dict:
    nested_field = f"{filter.field}.id"
    return {
        "nested": {
            "path": filter.field,
            "query": {"bool": {"must": [{"match": {nested_field: filter.value}}]}},
        }
    }


def _get_should_query(should_list: list[Should]) -> dict:
    # selected items by id in list
    return {
        "bool": {
            "should": [
                {"match": {should.field: should.value}} for should in should_list
            ]
        }
    }


def get_params(request: Request) -> dict[str, Union[str, dict]]:
    params: dict[str, Union[str, dict]] = {}
    for key, value in request.query_params.items():
        nested_key = key.removesuffix("]").split("[")
        if len(nested_key) == 2:
            params.setdefault(nested_key[0], {}).update({nested_key[1]: value})  # type: ignore
            continue
        params[key] = value

    return params
