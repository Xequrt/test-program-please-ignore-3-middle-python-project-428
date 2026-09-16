from psycopg.rows import dict_row


def get_flights(conn, origin, destination, start_utc, end_utc, passengers):
    sql = """
        SELECT 
            f.id,
            f.flightnumber,
            al.code AS al_code,
            al.name AS al_name,
            dc.code AS dc_code, 
            dc.name AS dc_name, 
            dc.country AS dc_country,
            ac.code AS ac_code, 
            ac.name AS ac_name, 
            ac.country AS ac_country,
            f.departureat,
            f.arrivalat,
            f.durationminutes,
            f.price_amount,
            f.seatsavailable
        FROM flights f
        JOIN cities dc ON f.departure_city = dc.code
        JOIN cities ac ON f.arrival_city = ac.code
        JOIN aviacompany al ON f.aviacompany = al.code
        WHERE f.departure_city = %s
          AND f.arrival_city = %s
          AND f.departureat >= %s 
          AND f.departureat < %s
          AND f.seatsavailable >= %s
    """
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql, (origin, destination, start_utc, end_utc, passengers))
        return cur.fetchall()


def get_flight_by_id(conn, flight_id):
    sql = """
        SELECT 
            f.id,
            f.flightnumber,
            al.code AS al_code,
            al.name AS al_name,
            dc.code AS dc_code, 
            dc.name AS dc_name, 
            dc.country AS dc_country,
            ac.code AS ac_code, 
            ac.name AS ac_name, 
            ac.country AS ac_country,
            f.departureat,
            f.arrivalat,
            f.durationminutes,
            f.price_amount,
            f.seatsavailable
        FROM flights f
        JOIN cities dc ON f.departure_city = dc.code
        JOIN cities ac ON f.arrival_city = ac.code
        JOIN aviacompany al ON f.aviacompany = al.code
        WHERE f.id = %s
    """
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql, (flight_id,))
        return cur.fetchone()
