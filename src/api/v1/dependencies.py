from fastapi import Query


async def common_parameters(
    query: str
    | None = Query(default=None, title="Запрос", description="Запрос для поиска"),
    number: int = Query(
        default=1, title="Номер страницы", description="Номер страницы"
    ),
    size: int = Query(
        default=50,
        title="Количество фильмов",
        description="Количество фильмов на странице",
    ),
) -> dict:
    return {"query": query, "number": number, "size": size}


async def film_search_parameters(
    query: str = Query(
        default=None,
        title="Название фильма",
        description="Часть названия фильма (Пример: dark sta )",
    ),
    page_size: int = Query(
        default=10,
        title="Количество фильмов",
        description="Количество фильмов на странице",
    ),
    page: int = Query(default=1, title="Номер страницы", description="Номер страницы"),
    sort: str = Query(
        default="",
        title="Сортировка",
        description="Сортировка полей (Пример: -imdb_rating)",
    ),
) -> dict:
    return {"query": query, "page": page, "page_size": page_size, "sort": sort}


async def film_list_parameters(
    page_size: int = Query(
        default=10,
        title="Количество фильмов",
        description="Количество фильмов на странице",
    ),
    page: int = Query(default=1, title="Номер страницы", description="Номер страницы"),
    sort: str = Query(
        default="",
        title="Сортировка",
        description="Сортировка полей (Пример: -imdb_rating)",
    ),
    genre: str = Query(
        default=None,
        title="Фильтр по жанру",
        description="Фильтр по жанру (Пример: sci-fi)",
    ),
) -> dict:
    return {"page": page, "page_size": page_size, "sort": sort, "genre": genre}
