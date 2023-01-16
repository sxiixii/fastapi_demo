from typing import Union

from fastapi import Query


async def common_parameters(
    query: Union[str, None] = Query(None, description="Запрос для поиска"),
    number: int = Query(1, description="Номер страницы"),
    size: int = Query(50, description="Количество фильмов на странице")
):
    return {'query': query, 'number': number, 'size': size}


async def film_search_parameters(
    query: str = Query(None, description="Часть названия фильма (Пример: dark sta )"),
    page_size: int = Query(10, description="Количество фильмов на странице"),
    page: int = Query(1, description="Номер страницы"),
    sort: str = Query("", description="Сортировка полей (Пример: imdb_rating:desc)")
):
    return {'query': query, 'page': page, 'page_size': page_size, 'sort': sort}


async def film_list_parameters(
    page_size: int = Query(10, description="Количество фильмов на странице"),
    page: int = Query(1, description="Номер страницы"),
    sort: str = Query("", description="Сортировка полей (Пример: imdb_rating:desc)"),
    genre: str = Query(None, description="Фильтр по жанру (Пример: sci-fi)")
):
    return {'page': page, 'page_size': page_size, 'sort': sort, 'genre': genre}
