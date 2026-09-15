from psycopg.rows import dict_row


def get_flights(conn, origin, destination, date, passengers):
    """Поиск рейсов: города как объекты, фильтр по местам в SQL."""
    sql = """
        SELECT f.id,
               dc.code AS dc_code, dc.name AS dc_name, dc.country AS dc_country,
               ac.code AS ac_code, ac.name AS ac_name, ac.country AS ac_country,
               f.departureAt, f.seatsAvailable
        FROM flights f
        JOIN cities dc ON f.departure_city = dc.code
        JOIN cities ac ON f.arrival_city = ac.code
        WHERE f.departure_city = %s
          AND f.arrival_city = %s
          AND f.departureAt::date = %s
          AND f.seatsAvailable >= %s
    """
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql, (origin, destination, date, passengers))
        return cur.fetchall()


def get_flight_by_id(conn, flight_id):
    """Один рейс по id. Возвращает None, если не найден."""
    sql = """
        SELECT f.id,
               dc.code AS dc_code, dc.name AS dc_name, dc.country AS dc_country,
               ac.code AS ac_code, ac.name AS ac_name, ac.country AS ac_country,
               f.departureAt, f.seatsAvailable
        FROM flights f
        JOIN cities dc ON f.departure_city = dc.code
        JOIN cities ac ON f.arrival_city = ac.code
        WHERE f.id = %s
    """
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql, (flight_id,))
        return cur.fetchone()
