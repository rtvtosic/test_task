import os

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from models import Document

from csv_parser import parse_data
from dotenv import load_dotenv


# ==== Подключение к БД и Elasticsearch ====
load_dotenv()
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")

elastic_host = os.getenv("ELASTIC_HOST")
elastic_port = os.getenv("ELASTIC_PORT")

engine = create_engine(f"postgresql+psycopg://{user}:{password}@{host}/{database}")
client = Elasticsearch(
    hosts=[f"http://{elastic_host}:{elastic_port}"]
)

# ==== Выгрузка данных из БД в индекс ====
# создание сессии и загрузка данных в БД

try:
    with Session(bind=engine) as db:
        documents = db.query(Document).all()
        total = len(documents)
        documents_dict = [{"_index": "documents", "_id": doc.id, "_source": {"id": doc.id, "text": doc.text}} for doc in documents]
        
        success, failed = bulk(client, documents_dict)
        print(f"Успешно: {success}, Failed: {len(failed)}")
        
        print(f"Всего документов: {total}")
            
except Exception as e:
    print(f"Возникла ошибка: {e}")

# поиск по тексту документа
phrase = "Слив ИНФОРМАЦИИ"
print(f"==== ПОИСК ПО ФРАЗЕ: {phrase}")
resp = client.search(
    index="documents",
    query={
        "match": {
            "text": phrase
        }
    },
    size=20
)
print(f"Всего документов нашлось: {resp['hits']['total']['value']}")

print(resp['hits']['hits'])