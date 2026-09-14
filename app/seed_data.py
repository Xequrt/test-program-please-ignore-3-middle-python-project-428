from db import get_connection
from datetime import date, timedelta

CITIES = [
    ("MOW", "Москва", "Россия"),
    ("LED", "Санкт-Петербург", "Россия"),
    ("AER", "Сочи", "Россия"),
    ("KZN", "Казань", "Россия"),
    ("SVX", "Екатеринбург", "Россия"),
    ("OVB", "Новосибирск", "Россия"),
    ("KGD", "Калининград", "Россия"),
]

AIRLINES = [
    ("SU", "Аэрофлот"),
    ("DP", "Победа"),
    ("S7", "S7 Airlines"),
    ("U6", "Уральские авиалинии"),
]

def seed_cities_and_airlines():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            for code, name, country in CITIES:
                cur.execute(
                    "INSERT INTO cities (code, name, country) VALUES (%s, %s, %s) ON CONFLICT (code) DO NOTHING",
                    (code, name, country),
                )

            for code, name in AIRLINES:
                cur.execute(
                    "INSERT INTO aviacompany (code, name) VALUES (%s, %s) ON CONFLICT (code) DO NOTHING",
                    (code, name),
                )
        
        conn.commit()
        print("Города и авиакомпании загружены")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при загрузке городов и авиакомпаний: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    seed_cities_and_airlines()
