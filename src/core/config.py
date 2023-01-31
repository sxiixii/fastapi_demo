import os
from logging import config as logging_config

from core.logger import LOGGING
from dotenv import load_dotenv
from pydantic import BaseSettings, Field

logging_config.dictConfig(LOGGING)
load_dotenv()


class Settings(BaseSettings):
    es_index: str | None = None
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_name: str = Field(..., env="PROJECT_NAME")
    redis_host: str = Field(..., env="REDIS_HOST")
    redis_port: int = Field(..., env="REDIS_PORT")
    elastic_host: str = Field(..., env="ELASTIC_HOST")
    elastic_port: int = Field(..., env="ELASTIC_PORT")
    cache_expires: int = 60 * 5

    class Config:
        env_file = ".env"


settings = Settings()
film_settings = Settings(
    es_index=os.getenv("FILM_ES_INDEX"),
)
person_settings = Settings(
    es_index=os.getenv("PERSON_ES_INDEX"),
)
genre_settings = Settings(
    es_index=os.getenv("GENRE_ES_INDEX"),
)
