from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from services.film import FilmService, get_film_service

router = APIRouter()


class API_Film(BaseModel):
    """
    Модель ответа API
    """

    id: str
    title: str


@router.get("/{film_id}", response_model=API_Film)
async def film_details(
    film_id: str, film_service: FilmService = Depends(get_film_service)
) -> API_Film:
    film = await film_service.get_by_id(film_id)
    if not film:  # Если фильм не найден, отдаём 404 статус
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return API_Film(id=film.id, title=film.title)
