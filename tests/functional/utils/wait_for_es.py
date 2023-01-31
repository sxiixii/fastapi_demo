import os

from backoff import backoff
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

es_host = f'{os.getenv("ELASTIC_HOST")}:{os.getenv("ELASTIC_PORT")}'


@backoff()
def connected_to_es(client):
    return client.ping()


if __name__ == "__main__":
    es_client = Elasticsearch([es_host])
    connected_to_es(es_client)
