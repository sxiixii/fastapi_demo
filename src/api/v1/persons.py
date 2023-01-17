from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from services.film import FilmService, get_film_service
from services.person import PersonService, get_person_service

from .dependencies import common_parameters
from .serializers import APIPerson, APIPersonFilms

router = APIRouter()


@router.get("/search", response_model=List[APIPerson])
async def persons_all(
    person_service: PersonService = Depends(get_person_service),
    commons: dict = Depends(common_parameters),
) -> List[APIPerson]:
    page = {"size": commons["size"], "number": commons["number"]}
    query = {"field": "name", "value": commons["query"]}
    persons = await person_service.get_by_params(query=query, page=page)
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="persons not found"
        )
    return [
        APIPerson(
            id=person.id,
            name=person.name,
            roles=person.roles,
        )
        for person in persons
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
    persons_film = await film_service.get_person_films(person)
    return [APIPersonFilms(role=item.role, films=item.films) for item in persons_film]
