from uuid import UUID

from pydantic import BaseModel

from models.base import BaseOrjsonModel


class RoleAndFilms(BaseModel):
    role: str
    film_ids: list[UUID]


class PersonModel(BaseOrjsonModel):
    name: str
    roles: list[RoleAndFilms]
