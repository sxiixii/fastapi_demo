from uuid import UUID

from models.base import BaseOrjsonModel
from pydantic import BaseModel


class Person(BaseModel):
    id: UUID
    name: str


class FilmModel(BaseOrjsonModel):
    title: str
    imdb_rating: float | None = 0.0
    genre: list[str] = []
    description: str | None = ""
    director: list[str] | None = []
    actors_names: list[str] = []
    writers_names: list[str] = []
    actors: list[Person] | None = []
    writers: list[Person] | None = []


class RoleAndFilmsModel(BaseModel):
    role: str
    films: list[FilmModel]
