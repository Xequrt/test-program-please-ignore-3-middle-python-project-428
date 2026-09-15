def serialize_flight(row):
    """Превращает строку из repositories в объект для ответа API."""
    return {
        "id": row["id"],
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
        "departureAt": row["departureat"],
        "seatsAvailable": row["seatsavailable"]
    }
