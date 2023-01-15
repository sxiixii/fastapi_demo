from models.base import BaseOrjsonModel
from models.film import FilmShortResponse


class PersonShortResponseForFilm(BaseOrjsonModel):
    '''
    укороченная модель ответа для Film о связанных Person
    '''
    name: str

class PersonShortResponse(PersonShortResponseForFilm):
    '''
    базовая модель ответа для Person
    '''
    full_name: str

class PersonDetailedReponce(PersonShortResponse):
    '''
    основная модель ответа для Person
    наследуется от базовой модели
    '''
    roles: list[str] = []
    films: list[FilmShortResponse] = []
