from uuid import UUID

from models.base import BaseOrjsonModel
from pydantic import BaseModel


class RoleAndFilms(BaseModel):
    role: str
    film_ids: list[UUID]


class PersonModel(BaseOrjsonModel):
    name: str
    roles: list[RoleAndFilms]
