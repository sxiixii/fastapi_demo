from typing import List
from uuid import UUID

from models.base import BaseOrjsonModel
from pydantic import BaseModel


class Person(BaseModel):
    id: UUID
    name: str


class FilmModel(BaseOrjsonModel):
    title: str
    imdb_rating: float | None = 0.0
    genre: List[str] = []
    description: str | None = ""
    director: List[str] | None = []
    actors_names: list[str] = []
    writers_names: list[str] = []
    actors: List[Person] | None = []
    writers: List[Person] | None = []


class RoleAndFilmsModel(BaseModel):
    role: str
    films: List[FilmModel]
