from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from services.genre import GenreService, get_genre_service
from .dependencies import common_parameters
from .serializers import APIGenre

router = APIRouter()


@router.get("/", response_model=list[APIGenre])
async def genres_all(
        genre_service: GenreService = Depends(get_genre_service),
        commons: dict = Depends(common_parameters),
) -> list[APIGenre]:
    page = {"size": commons["size"], "number": commons["number"]}
    query_filter = {"field": "name", "value": commons["query"]}
    genres = await genre_service.get_by_params(query_filter=query_filter, page=page)
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genres not found")
    return [
        APIGenre(
            id=genre.id,
            name=genre.name,
            description=genre.description,
            film_ids=genre.film_ids,
        )
        for genre in genres
    ]


@router.get("/{genre_id}", response_model=APIGenre)
async def person_details(
        genre_id: str, genre_service: GenreService = Depends(get_genre_service)
) -> APIGenre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genre not found")
    return APIGenre(**genre.dict())
