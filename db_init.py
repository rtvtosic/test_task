import os
from sqlalchemy import create_engine
from models import Base, Document
from dotenv import load_dotenv


# ==== Подключение к БД ====
load_dotenv()
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")

engine = create_engine(f"postgresql+psycopg://{user}:{password}@{host}/{database}")

# создание таблиц в базе данных
Base.metadata.create_all(bind=engine)
print("База данных и таблицы успешно созданы")
