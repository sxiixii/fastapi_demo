import time
import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

load_dotenv()

es_host = f'{os.getenv("ELASTIC_HOST")}:{os.getenv("ELASTIC_PORT")}'

if __name__ == '__main__':
    es_client = Elasticsearch([es_host])
    while True:
        if es_client.ping():
            break
        time.sleep(1)
