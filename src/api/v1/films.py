from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from services.film import FilmService, get_film_service

from typing import List

router = APIRouter()


class APIFilmList(BaseModel):
    id: str
    title: str
    imdb_rating: float
    # genre: List[Genre]


class APIFilm(BaseModel):
    """
    Модель ответа API
    """
    id: str
    title: str
    imdb_rating: float
    description: str
    # genre: List[str]
    # actors: List[str]
    # writers: List[str]
    # directors: List[str]


@router.get("/search", response_model=List[APIFilmList])
async def film_search(
    query: str = Query(None, description="Часть названия фильма (Пример: dark sta )"),
    page_size: int = Query(10, description="Количество фильмов на странице"),
    page: int = Query(1, description="Номер страницы"),
    sort: str = Query("", description="Сортировка полей (Пример: imdb_rating:desc)"),
    film_service: FilmService = Depends(get_film_service),
) -> List[APIFilmList]:
    """
    ручки film_search (полнотекстовый поиск по фильмам)
    """
    page = {
        'size': page_size,
        'number': page
    }
    films = await film_service.get_by_params(query=query, page=page, sort=sort)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="films not found")
    return [APIFilmList.parse_obj(film.dict(by_alias=True)) for film in films]


@router.get("/{film_id}", response_model=APIFilm)
async def film_details(
    film_id: str, film_service: FilmService = Depends(get_film_service)
) -> APIFilm:
    """
    ручки film_details (информация по фильму)
    """
    film = await film_service.get_by_id(film_id)
    if not film:  # Если фильм не найден, отдаём 404 статус
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return APIFilm(**film.dict(by_alias=True))


@router.get("/", response_model=List[APIFilmList])
async def film_list(
    page_size: int = Query(10, description="Количество фильмов на странице"),
    page: int = Query(1, description="Номер страницы"),
    sort: str = Query("", description="Сортировка полей (Пример: imdb_rating:desc)"),
    _filter: str = Query(None, description="Фильтр по жанру (Пример: sci-fi)"),
    film_service: FilmService = Depends(get_film_service),
) -> List[APIFilmList]:
    """
    ручки film_list (вывод списка фильмов)
    """
    page = {
        'size': page_size,
        'number': page
    }
    films = await film_service.get_by_params(page=page, sort=sort, _filter=_filter)
    return [APIFilmList.parse_obj(film.dict(by_alias=True)) for film in films]
