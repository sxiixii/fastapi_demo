from models.base import BaseOrjsonModel
from models.person import PersonShortResponseForFilm
from models.genre import GenreShortResponseForFilm

class FilmShortResponse(BaseOrjsonModel):
    '''
    базовая модель ответа для Film
    '''
    title: str

class FilmResponce(FilmShortResponse):
    '''
    основная модель ответа для Film
    наследуется от базовой модели
    '''
    imdb_rating: float | None = 0.0
    genre: list[GenreShortResponseForFilm] = []
    description: str | None = ""
    director: str | None = ""
    actors_names: list[str] = []
    writers_names: list[str] = []

class FilmDetailedResponse(FilmResponce):
    '''
    расширенная модель ответа для Film
    наследуется от основной модели
    '''
    actors: list[PersonShortResponseForFilm] = []
    writers: list[PersonShortResponseForFilm] = []



