from typing import List
from uuid import UUID

from models.base import BaseOrjsonModel
from pydantic import BaseModel


class RoleAndFilms(BaseModel):
    role: str
    film_ids: List[UUID]


class PersonModel(BaseOrjsonModel):
    name: str
    roles: List[RoleAndFilms]
