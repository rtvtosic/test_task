import os

from dotenv import load_dotenv
from elasticsearch import Elasticsearch

"""
Структура Индекса:

id - id из базы;
text - текст из структуры БД.
"""

load_dotenv()
elastic_host = os.getenv("ELASTIC_HOST")
elastic_port = os.getenv("ELASTIC_PORT")

# ==== подключение к elasticsearch ====
client = Elasticsearch(
    hosts=[f"http://{elastic_host}:{elastic_port}"]
)

# ==== создание индекса ====
mappings = {
    "properties": {
        "id": {"type": "integer"},
        "text": {"type": "text"}
    }
}

# client.indices.delete(index="documents")

if not client.indices.exists(index="documents"):
    client.indices.create(index="documents", mappings=mappings)