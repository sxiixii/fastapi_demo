from typing import Union

from fastapi import Query


async def common_parameters(
    query: Union[str, None] = Query(None, description="Запрос для поиска"),
    number: int = Query(1, description="Номер страницы"),
    size: int = Query(50, description="Количество фильмов на странице")
):
    return {'query': query, 'number': number, 'size': size}

