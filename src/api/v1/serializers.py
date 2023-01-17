from typing import List
from uuid import UUID

from pydantic import BaseModel


class RoleAndFilms(BaseModel):
    role: str
    film_ids: List[UUID]


class APIGenre(BaseModel):
    id: UUID
    name: str
    description: str
    film_ids: List[UUID]


class APIPersonBase(BaseModel):
    id: UUID
    name: str


class APIPerson(APIPersonBase):
    roles: List[RoleAndFilms]


class APIFilm(BaseModel):
    id: UUID
    title: str
    imdb_rating: float
    genre: List[str]


class APIFilmFull(APIFilm):
    description: str
    actors: List[APIPersonBase] | None = []
    writers: List[APIPersonBase] | None = []
    directors: List[APIPersonBase] | None = []


class APIPersonFilms(BaseModel):
    role: str
    films: List[APIFilm]
