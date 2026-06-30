import os
from sqlalchemy import create_engine
from dotenv import load_dotenv


load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")

engine = create_engine(f"postgresql+psycopg://{user}:{password}@{host}/{database}")

print("OK")