from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from services.film import FilmService, get_film_service
from typing import List

from .dependencies import film_search_parameters, film_list_parameters


router = APIRouter()


class APIFilmList(BaseModel):
    id: str
    title: str
    imdb_rating: float
    genre: List[str]


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
    commons: dict = Depends(film_search_parameters),
    film_service: FilmService = Depends(get_film_service),
) -> List[APIFilmList]:
    """
    ручки film_search (полнотекстовый поиск по фильмам)
    """
    page = {
        'size': commons['page_size'],
        'number': commons['page']
    }
    films = await film_service.get_by_params(query=commons['query'], page=page, sort=commons['sort'])
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
    commons: dict = Depends(film_list_parameters),
    film_service: FilmService = Depends(get_film_service)
) -> List[APIFilmList]:
    """
    ручки film_list (вывод списка фильмов)
    """
    page = {
        'size': commons['page_size'],
        'number': commons['page']
    }
    query_filter = {
        'field': 'genre',
        'value': commons['genre']
    }
    films = await film_service.get_by_params(page=page, sort=commons['sort'], query_filter=query_filter)
    return [APIFilmList.parse_obj(film.dict(by_alias=True)) for film in films]
