from models.base import BaseOrjsonModel


class GenreModel(BaseOrjsonModel):
    name: str
    description: str | None = ""
    films: list[str] = []
