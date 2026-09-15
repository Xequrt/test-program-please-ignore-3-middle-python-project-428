def serialize_flight(row):
    return {
        "id": str(row["id"]),
        "flightNumber": row["flightnumber"],
        "airline": {
            "code": row["al_code"],
            "name": row["al_name"]
        },
        "origin": {
            "code": row["dc_code"],
            "name": row["dc_name"],
            "country": row["dc_country"]
        },
        "destination": {
            "code": row["ac_code"],
            "name": row["ac_name"],
            "country": row["ac_country"]
        },
        "departureAt": _format_dt(row["departureat"]),
        "arrivalAt": _format_dt(row["arrivalat"]),
        "durationMinutes": row["durationminutes"],
        "price": {
            "amount": row["price_amount"],
            "currency": "RUB"
        },
        "seatsAvailable": row["seatsavailable"]
    }


def _format_dt(dt):
    if dt is None:
        return None
    return dt.isoformat().replace("+00:00", "Z")
