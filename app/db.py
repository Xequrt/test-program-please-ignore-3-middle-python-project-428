import os
from contextlib import contextmanager

from dotenv import load_dotenv
from psycopg_pool import ConnectionPool

load_dotenv()

_pool = None

def get_pool():
    global _pool
    if _pool is None:
        db_url = os.getenv("DATABASE_URL")
        _pool = ConnectionPool(
            db_url,
            min_size=2,
            max_size=10,
            open=True,
        )
    return _pool

@contextmanager
def get_connection():
    pool = get_pool()
    with pool.connection() as conn:
        conn.execute("SET TIME ZONE 'UTC'")
        yield conn

    