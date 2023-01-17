from uuid import UUID

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default=None):
    return orjson.dumps(v, default=default).decode()


class BaseOrjsonModel(BaseModel):
    id: UUID

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
