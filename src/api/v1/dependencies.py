from fastapi import Query

FILM_DETAILS_MESSAGE = "films not found"
GENRE_DETAILS_MESSAGE = "genres not found"
PERSON_DETAILS_MESSAGE = "persons not found"


class CommonQueryParams:
    def __init__(
        self,
        query: str
        | None = Query(
            default=None,
            title="Запрос",
            description="Поиск объекта",
        ),
        number: int = Query(
            default=1,
            title="Номер страницы",
            description="Номер страницы",
            gt=0,
            alias="page[number]",
        ),
        size: int = Query(
            default=50,
            title="Количество фильмов",
            description="Количество фильмов на странице",
            gt=0,
            alias="page[size]",
        ),
    ):
        self.query = query
        self.number = number
        self.size = size


class FilmQueryParams:
    def __init__(
        self,
        query: str = Query(
            default=None,
            title="Название фильма",
            description="Часть названия фильма (Пример: dark sta )",
        ),
        size: int = Query(
            default=10,
            title="Количество фильмов",
            description="Количество фильмов на странице",
            gt=0,
            le=10000,
            alias="page[size]",
        ),
        number: int = Query(
            default=1,
            title="Номер страницы",
            description="Номер страницы",
            gt=0,
            le=10000,
            alias="page[number]",
        ),
        sort: str = Query(
            default=None,
            title="Сортировка",
            description="Сортировка полей (Пример: -imdb_rating)",
        ),
    ):
        self.query = query
        self.size = size
        self.number = number
        self.sort = sort


class FilmFilterParams:
    def __init__(
        self,
        size: int = Query(
            default=10,
            title="Количество фильмов",
            description="Количество фильмов на странице",
            gt=0,
            le=10000,
            alias="page[size]",
        ),
        number: int = Query(
            default=1,
            title="Номер страницы",
            description="Номер страницы",
            gt=0,
            le=10000,
            alias="page[number]",
        ),
        sort: str = Query(
            default=None,
            title="Сортировка",
            description="Сортировка полей (Пример: -imdb_rating)",
        ),
        genre: str = Query(
            default=None,
            title="Фильтр по жанру",
            description="Фильтр по жанру (Пример: sci-fi)",
        ),
    ):
        self.size = size
        self.number = number
        self.sort = sort
        self.genre = genre
