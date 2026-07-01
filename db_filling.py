import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from models import Base, Document

from csv_parser import parse_data
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

# загрузка данных из csv-файла в правильном формате
data = parse_data(path='posts.csv')

# создание сессии и загрузка данных в БД
try:
    with Session(bind=engine) as db:
        # удаление данных перед загрузкой
        db.execute(text("TRUNCATE TABLE document RESTART IDENTITY"))
        db.commit()

        for obj in data:
            db.add(
                Document(text=obj[0],
                        created_date=obj[1],
                        rubrics=obj[2])
                )
        db.commit() # сохранение изменений в БД
    print("База данных успешно заполнена")
except Exception as e:
    print(f"Возникла ошибка: {e}")

