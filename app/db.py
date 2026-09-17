from dotenv import load_dotenv
import psycopg
import os

load_dotenv()

def get_connection():
    db_url = os.getenv("DATABASE_URL")
    conn = psycopg.connect(db_url)
    conn.execute("SET TIME ZONE 'UTC'")
    conn.commit()
    return conn

    