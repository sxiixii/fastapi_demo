from models.base import BaseOrjsonModel
from models.film import FilmShortResponse


class GenreShortResponseForFilm(BaseOrjsonModel):
    '''
    укороченная модель ответа для Film о связанных Genre
    '''
    name: str

class GenreShortResponse(GenreShortResponseForFilm):
    '''
    базовая модель ответа для Genre
    '''
    name: str
    description: str | None = ""


class GenreDetailedResponce(GenreShortResponse):
    '''
    основная модель ответа для Genre
    наследуется от базовой модели
    '''
    films: list[FilmShortResponse] = []
