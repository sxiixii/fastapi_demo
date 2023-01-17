from models.base import BaseOrjsonModel


class FilmModel(BaseOrjsonModel):
    title: str
    imdb_rating: float | None = 0.0
    genre: list[str] = []
    description: str | None = ""
    director: list[str] = []
    actors_names: list[str] = []
    writers_names: list[str] = []
    actors: list[dict] = []
    writers: list[dict] = []
