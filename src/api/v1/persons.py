from http import HTTPStatus

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from services.film import FilmService, get_film_service
from services.person import PersonService, get_person_service

from .dependencies import PERSON_DETAILS_MESSAGE, CommonQueryParams
from .serializers import APIPerson, APIPersonFilms

router = APIRouter()


@router.get("/search", response_model=list[APIPerson], summary="Поиск по персоне")
async def persons_all(
    person_service: PersonService = Depends(get_person_service),
    commons: CommonQueryParams = Depends(CommonQueryParams),
) -> list[APIPerson]:
    """
    полнотекстовый поиск по персоне
    """
    page = {"size": commons.size, "number": commons.number}
    query = {"field": "name", "value": commons.query}
    persons = await person_service.get_by_params(query=query, page=page)
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=PERSON_DETAILS_MESSAGE
        )
    return [
        APIPerson(
            id=person.id,
            name=person.name,
            roles=person.roles,
        )
        for person in persons
    ]


@router.get(
    "/{person_id}", response_model=APIPerson, summary="Поиск персоны по его UUID"
)
async def person_details(
    person_id: UUID, person_service: PersonService = Depends(get_person_service)
) -> APIPerson:
    """
    полная информация по персоне по его UUID
    """
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=PERSON_DETAILS_MESSAGE
        )
    return APIPerson(**person.dict())


@router.get(
    "/{person_id}/film",
    response_model=list[APIPersonFilms],
    summary="Вывод фильмов, в которых участвовала персона",
)
async def person_films(
    person_id: UUID,
    person_service: PersonService = Depends(get_person_service),
    film_service: FilmService = Depends(get_film_service),
) -> list[APIPersonFilms]:
    """
    Вывод фильмов в которых участвовала персона по UUID
    """
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=PERSON_DETAILS_MESSAGE
        )
    persons_film = await film_service.get_person_films(person)
    return [APIPersonFilms(role=item.role, films=item.films) for item in persons_film]
