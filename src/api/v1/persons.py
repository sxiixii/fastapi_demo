from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from services.person import PersonService, get_person_service
from services.film import FilmService, get_film_service

from .dependencies import common_parameters

router = APIRouter()


class APIPerson(BaseModel):
    id: str
    full_name: str
    role: str
    film_ids: list[str]


class APIPersonFilms(BaseModel):
    id: str
    title: str
    imdb_rating: float


@router.get("/search", response_model=List[APIPerson])
async def persons_all(
        person_service: PersonService = Depends(get_person_service),
        commons: dict = Depends(common_parameters)
) -> List[APIPerson]:
    page = {
        'size': commons['size'],
        'number': commons['number']
    }
    persons = await person_service.get_by_params(query=commons['query'], page=page)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="persons not found")
    return [
        APIPerson(
            id=person.id,
            full_name=person.full_name,
            role=person.role,
            film_ids=person.film_ids,
        ) for person in persons
    ]


@router.get("/{person_id}", response_model=APIPerson)
async def person_details(
    person_id: str, person_service: PersonService = Depends(get_person_service)
) -> APIPerson:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="person not found")
    return APIPerson(**person.dict())


@router.get("/{person_id}/film", response_model=List[APIPersonFilms])
async def person_films(
        person_id: str,
        person_service: PersonService = Depends(get_person_service),
        film_service: FilmService = Depends(get_film_service),
) -> List[APIPersonFilms]:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="person not found")
    person_films = await film_service.get_by_list_of_id(person.film_ids)
    return [
        APIPersonFilms(
            id=film.id,
            title=film.title,
            imdb_rating=film.imdb_rating
        ) for film in person_films
    ]
