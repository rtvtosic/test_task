import os
import uvicorn

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Document

from dotenv import load_dotenv


# ==== Подключение к БД ====
load_dotenv()
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")
engine = create_engine(f"postgresql+psycopg://{user}:{password}@{host}/{database}")


app = FastAPI()

@app.get("/documents/")
def get_all_documents():
    documents_dict = []

    try:
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
    except Exception as e:
        raise HTTPException()


@app.get("/documents/{doc_id}")
def get_document_by_id(doc_id: int):
    
    with Session(bind=engine) as db:
        doc = db.get(Document, doc_id)
        if doc == None:
            raise HTTPException(status_code=404, detail="Document Not Found")
        return {
                "id": doc.id,
                "text": doc.text,
                "created_date": doc.created_date,
                 "rubrics": doc.rubrics
                } 
    
    
    

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
