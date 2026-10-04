import os

from dotenv import load_dotenv
from psycopg.errors import Error
from yoyo import get_backend, read_migrations

load_dotenv()

if __name__ == "__main__":
    database_url = os.getenv("DATABASE_URL")

    if database_url is not None and database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)

    try:
        backend = get_backend(database_url)
        migrations = read_migrations('migrations')        

        with backend.lock():
            migrations_to_apply = backend.to_apply(migrations)

            if migrations_to_apply:
                backend.apply_migrations(migrations_to_apply)
                print('Миграции применены')
            else:
                print('Нечего применять')
    except Error as e:
        print(f"Ошибка при применении миграций: {e}")
        raise
