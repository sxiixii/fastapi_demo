from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query

from pydantic import BaseModel

# from models.film import Genre, Person
from models.mixins import UUIDMixin
from services.film import FilmService, get_film_service

from typing import List

router = APIRouter()


class API_FilmList(UUIDMixin, BaseModel):
    title: str
    imdb_rating: float
    # genre: List[Genre]


class API_Film(UUIDMixin, BaseModel):
    """
    Модель ответа API
    """

    title: str
    imdb_rating: float
    description: str
    # genre: List[Genre]
    # actors: List[Person]
    # writers: List[Person]
    # directors: List[Person]


@router.get("/{film_id}", response_model=API_Film)
async def film_details(
    film_id: str, film_service: FilmService = Depends(get_film_service)
) -> API_Film:
    """
    ручки film_details (информация по фильму)
    """
    film = await film_service.get_by_id(film_id)
    if not film:  # Если фильм не найден, отдаём 404 статус
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return API_Film(**film.dict(by_alias=True))


@router.get("/", response_model=List[API_FilmList])
async def film_list(
    page_size: int = Query(10, description="Количество фильмов на странице"),
    page: int = Query(1, description="Номер страницы"),
    sort: str = Query("", description="Сортировка полей (Пример: imdb_rating:desc)"),
    genre: str = Query(None, description="Фильтр по жанру (Пример: sci-fi)"),
    film_service: FilmService = Depends(get_film_service),
) -> List[API_FilmList]:
    """
    ручки film_list (вывод списка фильмов)
    """
    films = await film_service.get_by_params(
        page_size=page_size, page=page, sort=sort, genre=genre
    )
    return [API_FilmList.parse_obj(film.dict(by_alias=True)) for film in films]


@router.get("/search", response_model=List[API_FilmList])
async def film_search(
    page_size: int = Query(10, description="Количество фильмов на странице"),
    page: int = Query(1, description="Номер страницы"),
    sort: str = Query("", description="Сортировка полей (Пример: imdb_rating:desc)"),
    query: str = Query(None, description="Часть названия фильма (Пример: dark sta )"),
    film_service: FilmService = Depends(get_film_service),
) -> List[API_FilmList]:
    """
    ручки film_search (полнотекстовый поиск по фильмам)
    """
    films = await film_service.get_by_params(
        page_size=page_size, page=page, sort=sort, query=query
    )
    return [API_FilmList.parse_obj(film.dict(by_alias=True)) for film in films]
