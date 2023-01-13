from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from services.genre import GenreService, get_genre_service

from .dependencies import common_parameters

router = APIRouter()


class APIGenre(BaseModel):
    id: str
    name: str


@router.get("/", response_model=List[APIGenre])
async def genres_all(
        genre_service: GenreService = Depends(get_genre_service),
        commons: dict = Depends(common_parameters)
) -> List[APIGenre]:
    page = {
        'size': commons['size'],
        'number': commons['number']
    }
    genres = await genre_service.get_by_params(query=commons['query'], page=page)
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genres not found")
    return [
        APIGenre(
            id=genre.id,
            name=genre.name,
        ) for genre in genres
    ]


@router.get("/{genre_id}", response_model=APIGenre)
async def person_details(
    genre_id: str, genre_service: GenreService = Depends(get_genre_service)
) -> APIGenre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genre not found")
    return APIGenre(**genre.dict())
