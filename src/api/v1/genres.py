from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from services.genre import GenreService, get_genre_service

from .dependencies import GENRE_DETAILS_MESSAGE, CommonQueryParams
from .serializers import APIGenre

router = APIRouter()


@router.get("/", response_model=list[APIGenre], summary="поиск по жанрам")
async def genres_all(
    genre_service: GenreService = Depends(get_genre_service),
    commons: CommonQueryParams = Depends(CommonQueryParams),
) -> list[APIGenre]:
    """
    полнотекстовый поиск по жанрам
    """
    page = {"size": commons.size, "number": commons.number}
    filter_parameter = {"field": "name", "value": commons.query}
    params = {"page": page, "filter_parameter": filter_parameter}
    genres = await genre_service.get(params)
    if genres is None:
        return []
    return [
        APIGenre(
            id=genre.id,
            name=genre.name,
            description=genre.description,
            film_ids=genre.film_ids,
        )
        for genre in genres
    ]


@router.get("/{genre_id}", response_model=APIGenre, summary="поиск жанра по UUID")
async def person_details(
    genre_id: UUID, genre_service: GenreService = Depends(get_genre_service)
) -> APIGenre:
    """
    полная информация по жанру по его UUID
    """
    genre = await genre_service.get(genre_id)
    if not genre:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=GENRE_DETAILS_MESSAGE
        )
    return APIGenre(**genre.dict())
