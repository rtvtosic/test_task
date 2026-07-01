import uvicorn

from database import get_db
from fastapi import FastAPI, HTTPException, Depends

from sqlalchemy import desc
from sqlalchemy.orm import Session
from models import Document

from elasticsearch import NotFoundError
from config import client


app = FastAPI()

@app.get("/documents/")
def get_all_documents(db: Session = Depends(get_db)):
    """вывод всех документов"""
    documents_dict = []

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
    

# получение документа по id
@app.get("/documents/{doc_id}")
def get_document_by_id(doc_id: int, db: Session = Depends(get_db)):
    """Получение документа по id"""
    
    doc = db.get(Document, doc_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="Document Not Found")
    
    return {
            "id": doc.id,
            "text": doc.text,
            "created_date": doc.created_date,
            "rubrics": doc.rubrics
            }


# поиск документа по тексту
@app.post("/search")
def search_docs_by_text(text: str, db: Session = Depends(get_db)):
    """Поиск документа по тексту"""

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
    query = db.query(Document).filter(
        Document.id.in_(document_ids)
    ).order_by(desc(Document.created_date)).all()

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

# удалять документ из БД и индекса по полю id.
@app.delete("/documents/{doc_id}")
def delete_doc_by_id(doc_id: int, db: Session = Depends(get_db)):
    """Удаление документа из БД и индекса по полю id"""

    # удаление из Postgres
    doc_to_delete = db.get(Document, doc_id)

    if doc_to_delete is None:
        raise HTTPException(status_code=404, detail="Document Not Found")
        
    db.delete(doc_to_delete)
    db.commit()
    
    # удаление из Elasticsearch
    try:
        client.delete(index="documents", id=str(doc_id))
    except NotFoundError:
        pass

    return {"detail": "Document deleted"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
