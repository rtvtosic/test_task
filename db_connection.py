import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

conn = psycopg.connect(
    dbname=os.getenv("DB_NAME"),
    host=os.getenv("DB_HOST"),
    port = os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)
cursor = conn.cursor()
print("Подключение установлено")

cursor.execute("select 'hello';")
ans = cursor.fetchall()
print(f"Результат выполнения запроса: {ans}")
cursor.close()
conn.close()