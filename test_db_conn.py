import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


# ==== Подключение к БД ====
load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")

engine = create_engine(f"postgresql+psycopg://{user}:{password}@{host}/{database}")

# проверка соединения
with engine.connect() as conn:
    ans = conn.execute(text('select 1'))
    print(ans.scalar())

