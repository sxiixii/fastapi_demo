from uuid import UUID

import orjson
from models.base import orjson_dumps
from pydantic import BaseModel


class BaseOrjsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class RoleAndFilms(BaseOrjsonModel):
    role: str
    film_ids: list[UUID]


class APIGenre(BaseOrjsonModel):
    id: UUID
    name: str
    description: str
    film_ids: list[UUID]


class APIPersonBase(BaseOrjsonModel):
    id: UUID
    name: str


class APIPerson(APIPersonBase):
    roles: list[RoleAndFilms]


class APIFilm(BaseOrjsonModel):
    id: UUID
    title: str
    imdb_rating: float
    genre: list[str]


class APIFilmFull(APIFilm):
    description: str
    actors: list[APIPersonBase] | None = []
    writers: list[APIPersonBase] | None = []
    directors: list[APIPersonBase] | None = []


class APIPersonFilms(BaseOrjsonModel):
    role: str
    films: list[APIFilm]
