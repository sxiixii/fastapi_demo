import os

import redis
from backoff import backoff
from dotenv import load_dotenv

load_dotenv()


@backoff()
def connected_to_redis(client):
    return client.ping()


if __name__ == "__main__":
    redis_client = redis.Redis(
        host=os.getenv("REDIS_HOST"),
        port=int(os.getenv("REDIS_PORT")),
        db=0,
    )
    connected_to_redis(redis_client)
