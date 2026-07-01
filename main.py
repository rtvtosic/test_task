import os
import uvicorn

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Document

from elasticsearch import Elasticsearch

from dotenv import load_dotenv


# ==== Подключение к БД и Elasticsearch====
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


app = FastAPI()

@app.get("/documents/")
def get_all_documents():
    documents_dict = []

    
    with Session(bind=engine) as db:
        documents = db.query(Document).all()
        for doc in documents:

            documents_dict.append(
                {
                    "id": doc.id,
                    "text": doc.text,
                    "created_date": doc.created_date,
                    "rubrics": doc.rubrics
                }

            )
    return documents_dict
    


@app.get("/documents/{doc_id}")
def get_document_by_id(doc_id: int):
    
    with Session(bind=engine) as db:
        doc = db.get(Document, doc_id)
        if doc is None:
            raise HTTPException(status_code=404, detail="Document Not Found")
        return {
                "id": doc.id,
                "text": doc.text,
                "created_date": doc.created_date,
                 "rubrics": doc.rubrics
                }


@app.post("/search")
def search_docs_by_text(text: str):
    # ==== Поиск нужных id в индексе в Elasticsearch ====
    document_ids = []
    result_documents = []

    resp = client.search(
        index="documents",
        query={
            "match": {
                "text": text
            }
        },
        size=20
    )

    for doc in resp['hits']['hits']:
        document_ids.append(doc['_source']['id'])
    
    # ==== Поиск данных по id в Postgres ====
    with Session(bind=engine) as db:
        query = db.query(Document).filter(
            Document.id.in_(document_ids)
        ).order_by(Document.created_date).all()

        for doc in query:
            result_documents.append(
                {
                    "id": doc.id,
                    "created_date": doc.created_date,
                    "text": doc.text,
                    "rubrics": doc.rubrics
                }
            )
    
    return result_documents


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
