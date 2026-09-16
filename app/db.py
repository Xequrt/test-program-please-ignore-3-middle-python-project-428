from dotenv import load_dotenv
import psycopg
import os

load_dotenv()

def get_connection():
    db_url = os.getenv("DATABASE_URL")
    return psycopg.connect(db_url)

    