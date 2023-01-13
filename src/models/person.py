from models.base import BaseOrjsonModel


class PersonModel(BaseOrjsonModel):
    full_name: str
    role: str
    film_ids: list[str] = []
