import os

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

from .testdata.es_index import genres_index, movies_index, persons_index

load_dotenv()

ELASTIC_HOST = f'{os.getenv("ELASTIC_HOST")}:{os.getenv("ELASTIC_PORT")}'


class TestBaseSettings(BaseSettings):
    es_index: str | None = None
    es_index_mapping: dict | None = None
    es_id_field: str = Field(..., env="ID_FIELD")
    es_host: str = Field(ELASTIC_HOST)

    redis_host: str = Field(..., env="REDIS_HOST")
    redis_port: str = Field(..., env="REDIS_PORT")

    service_url: str = Field(..., env="SERVICE_URL")

    class Config:
        env_file = ".env.docker", ".env"


base_settings = TestBaseSettings()
film_settings = TestBaseSettings(
    es_index=os.getenv("FILM_ES_INDEX"),
    es_index_mapping=movies_index,
)
person_settings = TestBaseSettings(
    es_index=os.getenv("PERSON_ES_INDEX"),
    es_index_mapping=persons_index,
)
genre_settings = TestBaseSettings(
    es_index=os.getenv("GENRE_ES_INDEX"),
    es_index_mapping=genres_index,
)
