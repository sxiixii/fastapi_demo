from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class APIGenre(BaseModel):
    id: UUID
    name: str
    description: str
    film_ids: List[UUID]


class APIPerson(BaseModel):
    id: str
    full_name: str
    role: str
    film_ids: List[UUID]


class Person(BaseModel):
    id: UUID
    name: str


class APIFilm(BaseModel):
    id: UUID
    title: str
    imdb_rating: float


class APIFilmFull(APIFilm):
    genre: List[str]
    description: str
    actors: Optional[List[Person]] = []
    writers: Optional[List[Person]] = []
    directors: Optional[List[Person]] = []
