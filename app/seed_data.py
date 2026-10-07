from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from db import get_connection
from psycopg.errors import Error

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

DEPARTURE_HOURS = [8, 18]

CITY_CODES = [c[0] for c in CITIES]
AIRLINE_CODES = [a[0] for a in AIRLINES]

MOSCOW = ZoneInfo("Europe/Moscow")

def seed_cities_and_airlines():
    with get_connection() as conn:
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
            
            print("Города и авиакомпании загружены")
        except Error as e:
            print(f"Ошибка при загрузке городов и авиакомпаний: {e}")
            raise

def seed_flights():
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                today = datetime.now(MOSCOW).date()
                
                cur.execute("SELECT MAX(departureAt) FROM flights")
                result = cur.fetchone()
                last_departure_utc = result[0] if result[0] else None
                
                if last_departure_utc:
                    last_flight_date = last_departure_utc.astimezone(MOSCOW).date()
                    days_difference = (last_flight_date - today).days
                    start_offset = max(0, days_difference + 1)
                else:
                    start_offset = 0
                
                rows = []
                count = 0

                for day_offset in range(start_offset, 30):
                    current_date = today + timedelta(days=day_offset)

                    for from_city in CITY_CODES:
                        for to_city in CITY_CODES:
                            if from_city == to_city:
                                continue

                            for i in range(2):
                                dep_hour = DEPARTURE_HOURS[i]
                                departure_at = datetime.combine(
                                    current_date,
                                    time(dep_hour, 0),
                                    tzinfo=MOSCOW
                                )
                                duration_minutes = 120
                                arrival_at = departure_at + timedelta(minutes=duration_minutes)
                                
                                from_idx = CITY_CODES.index(from_city)
                                to_idx = CITY_CODES.index(to_city)
                                route_number = from_idx * len(CITY_CODES) + to_idx
                                flight_suffix = route_number * 10 + i
                                
                                airline_code = AIRLINE_CODES[count % len(AIRLINE_CODES)]
                                flight_number = f"{airline_code}{1000 + flight_suffix}"
                                price_amount = 3000 + (count % 5500)
                                seats_available = 30 + (count % 61)

                                rows.append((
                                    airline_code, from_city, to_city,
                                    flight_number, duration_minutes, departure_at,
                                    arrival_at, price_amount, seats_available
                                ))
                                count += 1

                cur.executemany(
                    """
                    INSERT INTO flights (
                        aviacompany, departure_city, arrival_city,
                        flightNumber, durationMinutes, departureAt,
                        arrivalAt, price_amount, seatsAvailable
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (flightNumber, departureAt) DO NOTHING
                    """,
                    rows
                )
            print(f"Сгенерировано {count} рейсов")
        except Error as e:
            print(f"Ошибка: {e}")
            raise
if __name__ == "__main__":
    seed_cities_and_airlines()
    seed_flights()
