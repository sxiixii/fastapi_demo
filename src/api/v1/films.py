from http import HTTPStatus
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from services.film import FilmService, get_film_service

from .dependencies import film_list_parameters, film_search_parameters
from .serializers import APIFilm, APIFilmFull

router = APIRouter()


@router.get("/search", response_model=List[APIFilm])
async def film_search(
    commons: dict = Depends(film_search_parameters),
    film_service: FilmService = Depends(get_film_service),
) -> List[APIFilm]:
    """
    ручки film_search (полнотекстовый поиск по фильмам)
    """
    page = {"size": commons["page_size"], "number": commons["page"]}
    query = {"field": "title", "value": commons["query"]}
    films = await film_service.get_by_params(
        query=query, page=page, sort=commons["sort"]
    )
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="films not found")
    return [APIFilm.parse_obj(film.dict(by_alias=True)) for film in films]


@router.get("/{film_id}", response_model=APIFilmFull)
async def film_details(
    film_id: UUID, film_service: FilmService = Depends(get_film_service)
) -> APIFilmFull:
    """
    ручки film_details (информация по фильму)
    """
    film = await film_service.get_by_id(film_id)
    if not film:  # Если фильм не найден, отдаём 404 статус
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return APIFilmFull(**film.dict(by_alias=True))


@router.get("/", response_model=List[APIFilm])
async def film_list(
    commons: dict = Depends(film_list_parameters),
    film_service: FilmService = Depends(get_film_service),
) -> List[APIFilm]:
    """
    ручки film_list (вывод списка фильмов)
    """
    page = {"size": commons["page_size"], "number": commons["page"]}
    query_filter = {"field": "genre", "value": commons["genre"]}
    films = await film_service.get_by_params(
        page=page, sort=commons["sort"], query_filter=query_filter
    )
    return [APIFilm.parse_obj(film.dict(by_alias=True)) for film in films]
