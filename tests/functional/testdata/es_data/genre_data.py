import uuid
from random import choices

from .film_data import film_ids

GENRE_CONTROL_UUID = "dc686a0e-06e4-48a8-939d-3758c89d14b8"

genres = [
    "Action",
    "Adventure",
    "Comedy",
    "Crime",
    "Fantasy",
    "Historical",
    "Horror",
    "Romance",
]

genres_data = [
    {
        "id": str(uuid.uuid4()),
        "name": genre,
        "description": "some descriptions",
        "film_ids": choices(film_ids, k=5),
    }
    for genre in genres
]
control_data = {
    "id": GENRE_CONTROL_UUID,
    "name": "Sci-Fi",
    "description": "some descriptions",
    "film_ids": choices(film_ids, k=5),
}
genres_data.append(control_data)
