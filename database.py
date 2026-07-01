from config import db_engine
from sqlalchemy.orm import Session


def get_db():
    db = Session(bind=db_engine)
    try:
        yield db
    finally:
        db.close()
