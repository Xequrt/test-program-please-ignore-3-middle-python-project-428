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
        "departureAt": row["departureat"].strftime("%Y-%m-%dT%H:%M:%SZ"),
        "arrivalAt":   row["arrivalat"].strftime("%Y-%m-%dT%H:%M:%SZ"),
        "durationMinutes": row["durationminutes"],
        "price": {
            "amount": row["price_amount"],
            "currency": "RUB"
        },
        "seatsAvailable": row["seatsavailable"]
    }

def serialize_booking(booking_code, status, flight_row, passengers, contact, total_price, created_at):
    return {
        "code": booking_code,
        "status": status,
        "flight": serialize_flight(flight_row),
        "passengers": [p.model_dump() for p in passengers],
        "contact": contact.model_dump(),
        "totalPrice": {
            "amount": total_price,
            "currency": "RUB"
        },
        "createdAt": created_at.strftime("%Y-%m-%dT%H:%M:%SZ")

    }

