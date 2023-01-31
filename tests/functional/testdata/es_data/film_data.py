from datetime import datetime
from uuid import uuid4

film_ids = [
    "fbf15226-49bc-442a-b3fb-dafa3af8c607",
    "b73a26f1-319e-4b6b-acf1-03ea5d901859",
    "b39da891-96f2-4b48-98f5-fa8c90ec2996",
    "5e286737-2508-45de-a8c8-7b24c28d74fd",
    "b219d3de-6d59-4e28-b182-71476f13d9df",
    "07f70f73-3f38-46e9-8e83-a188e5072612",
    "8a8b1fbc-7f95-422b-a7fb-7d509f5e49aa",
    "dc3d4fe8-5111-475f-9084-ac994b25af9c",
    "10bbbb38-0fe8-4b32-addf-f9aa20fd54f6",
    "bb886697-c0b1-48a7-b21a-c516f0c9c7dd",
    "bb715308-3902-4a8e-b578-18e91f0e27bd",
    "f35423bc-99f7-4578-b66e-aaaef39d2825",
    "547c2b88-74ae-4aee-91dd-9c9b03f625a8",
    "72b6472b-e658-4e6e-ba0e-b3f21a8b281e",
    "9d7c201e-1b46-4527-a37d-f1c9553cf6ce",
    "763e29c1-172e-42c2-a7e2-ad09c23c9af6",
    "187bfe87-a824-4df7-936e-0c34e8745d0f",
    "818efc3d-b71a-4749-ae1c-a9c04888b0f1",
    "7bbe9fe2-97d5-458e-be6b-fa3af1905977",
    "7ffd8a70-ba69-4903-af98-4c16bb9e626e",
]

films_data = [
    {
        "id": id,
        "imdb_rating": 8.5,
        "genre": ["Action", "Sci-Fi"],
        "title": "The Star",
        "description": "New World",
        "director": ["Allison", "Allison"],
        "actors_names": ["Brittni", "Allison"],
        "writers_names": ["Allison", "Brittni"],
        "actors": [
            {"id": str(uuid4()), "name": "Brook"},
        ],
        "writers": [
            {"id": str(uuid4()), "name": "Cayla"},
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "film_work_type": "movie",
    }
    for id in film_ids
]
