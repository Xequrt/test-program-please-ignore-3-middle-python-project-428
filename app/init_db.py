from db import get_connection
from psycopg.errors import Error

CREATE_TABLES = """
CREATE TABLE IF NOT EXISTS cities (
    code VARCHAR(50) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    country VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS aviacompany (
    code VARCHAR(20) PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS flights (
    id SERIAL PRIMARY KEY,
    aviacompany VARCHAR(20) REFERENCES aviacompany(code),
    departure_city VARCHAR(50) REFERENCES cities(code),
    arrival_city VARCHAR(50) REFERENCES cities(code),
    flightNumber VARCHAR(50),
    durationMinutes integer, CHECK (durationMinutes BETWEEN 80 AND 280),
    departureAt TIMESTAMPTZ,
    arrivalAt TIMESTAMPTZ,
    price_amount integer, CHECK (price_amount BETWEEN 3000 AND 8500),
    seatsAvailable integer, CHECK (seatsAvailable BETWEEN 10 AND 90),
    UNIQUE (flightNumber, departureAt)
);

CREATE TABLE IF NOT EXISTS bookings (
    id SERIAL PRIMARY KEY,
    flight_id integer REFERENCES flights(id),
    code VARCHAR(20) UNIQUE,
    status VARCHAR(50),
    totalPrice integer,
    createdAt TIMESTAMPTZ,
    updatedAt TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    email VARCHAR(50),
    phone VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS passengers (
    id SERIAL PRIMARY KEY,
    booking_id integer REFERENCES bookings(id),
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(100),
    birthday DATE,
    passportNumber VARCHAR(100)
);
"""

if __name__ == "__main__":
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(CREATE_TABLES)

        conn.commit()
        print('Схема БД создана')
    except Error as e:
        print(f"Ошибка при создании схемы БД: {e}")
        conn.rollback()
    finally:
        conn.close()
