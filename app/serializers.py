def serialize_flight(row):
    return {
        "id": row["id"],
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
        "departureAt": row["departureat"],
        "arrivalAt": row["arrivalat"],
        "durationMinutes": row["durationminutes"],
        "price": {
            "amount": row["price_amount"],
            "currency": "RUB"
        },
        "seatsAvailable": row["seatsavailable"]
    }


