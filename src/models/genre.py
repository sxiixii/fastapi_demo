from typing import List

from models.base import BaseOrjsonModel


class GenreModel(BaseOrjsonModel):
    name: str
    description: str | None
    film_ids: List[str] = []
