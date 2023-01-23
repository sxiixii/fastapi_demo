from typing import Any

from pydantic import BaseModel
from pydantic.types import PositiveInt


class Page(BaseModel):
    size: PositiveInt = 50
    number: PositiveInt = 1


class Filter(BaseModel):
    field: str
    value: str | None


class ValidParameters(BaseModel):
    query: dict | None
    sort: str | None
    filter_parameter: Filter | None
    page: Page | None


class QueryParameterHandler:
    def __init__(self):
        self.params: ValidParameters | None = None

    def get_es_query_body(self, raw_params: dict) -> dict[str | Any]:
        self.params = self._validate_raw_params(**raw_params)
        es_query_body: dict[str, Any] = {}
        return self._set_sort_params(
            self._set_default_query(
                self._set_filter_params(
                    self._set_query(self._set_page_params(es_query_body))
                )
            )
        )

    def _validate_raw_params(
        self,
        query: dict = None,
        sort: str = None,
        page: dict = None,
        filter_parameter: dict = None,
    ) -> ValidParameters:
        if filter_parameter is not None:
            filter_parameter = Filter(
                field=filter_parameter["field"],
                value=filter_parameter["value"],
            )
        return ValidParameters(
            query=query,
            sort=sort,
            filter_parameter=filter_parameter,
            page=Page(**page),
        )

    def _set_page_params(self, es_query_body: dict) -> dict:
        if self.params.page is not None:
            es_query_body["from"] = (
                self.params.page.number - 1
            ) * self.params.page.size
            es_query_body["size"] = self.params.page.size
        return es_query_body

    def _set_query(self, es_query_body: dict) -> dict:
        if self.params.query is not None and self.params.query["value"] is not None:
            es_query_body.setdefault("query", {}).update(
                self._get_search_query(self.params.query)
            )
        return es_query_body

    def _set_filter_params(self, es_query_body: dict) -> dict:
        if (
            self.params.filter_parameter is not None
            and self.params.filter_parameter.value is not None
        ):
            es_query_body.setdefault("query", {}).update(
                self._get_filter_query(self.params.filter_parameter)
            )
        return es_query_body

    def _set_default_query(self, es_query_body: dict) -> dict:
        if "query" not in es_query_body:
            es_query_body["query"] = {"match_all": {}}
        return es_query_body

    def _set_sort_params(self, es_query_body: dict) -> dict:
        if self.params.sort is not None:
            field = self.params.sort.removeprefix("-")
            direction = "desc" if self.params.sort.startswith("-") else "asc"
            es_query_body["sort"] = {field: {"order": direction}}
        return es_query_body

    def _get_search_query(self, query: dict) -> dict:
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

    def _get_filter_query(self, filter_parameter: Filter) -> dict:
        return {"match": {filter_parameter.field: {"query": filter_parameter.value}}}
