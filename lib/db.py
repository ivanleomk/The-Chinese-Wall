from psycopg2 import pool
from datetime import datetime
from settings import get_settings

connection_pool = pool.ThreadedConnectionPool(
    minconn=1, maxconn=10, dsn=get_settings().DATABASE_URL
)


def insert_prompt_into_db(prompt: str, level: str, response_result: str):
    conn = connection_pool.getconn()
    timestamp = datetime.now()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO messages (level, prompt, response,timestamp) VALUES (%s, %s, %s,%s)",
                (level, prompt, response_result, timestamp),
            )
        conn.commit()
    finally:
        connection_pool.putconn(conn)


def get_all_logs():
    conn = connection_pool.getconn()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM messages")
            rows = cursor.fetchall()
            return rows
    finally:
        connection_pool.putconn(conn)
