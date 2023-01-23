import time
import os
import redis

from dotenv import load_dotenv

load_dotenv()


if __name__ == '__main__':
    redis_client = redis.Redis(
        host=os.getenv("REDIS_HOST"),
        port=int(os.getenv("REDIS_PORT")),
        db=0,
    )
    while True:
        if redis_client.ping():
            break
        time.sleep(1)
