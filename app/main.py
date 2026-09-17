from pathlib import Path
from datetime import timezone, datetime, timedelta
from zoneinfo import ZoneInfo
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
import random, string
from pydantic import BaseModel
from psycopg.errors import UniqueViolation

from .db import get_connection
from .sql import get_flights, get_flight_by_id, create_booking
from .serializers import serialize_flight, serialize_booking

class ContactRequest(BaseModel):
    email: str
    phone: str

class PassengerRequest(BaseModel):
    firstName: str
    lastName: str
    dateOfBirth: str
    documentNumber: str

class CreateBookingRequest(BaseModel):
    flightId: str
    contact: ContactRequest
    passengers: list[PassengerRequest]

def generate_booking_code():
    alphabet = string.ascii_uppercase + string.digits
    return "".join(random.choices(alphabet, k=6))

def create_app() -> FastAPI:
    app = FastAPI()
    conn = get_connection()

    @app.exception_handler(RequestValidationError)
    def validation_exception_handler(request, exc):
        print(exc.errors())
        return JSONResponse(
            status_code=400,
            content={"code": "validation_error", "message": "Invalid request parameters"}
        )

    @app.get("/api/health")
    def get_health():
        return {"status": "ok"}

    @app.get("/api/cities")
    def get_cities():
        with conn.cursor() as cur:
            cur.execute("SELECT code, name, country FROM cities")
            rows = cur.fetchall()
        return [
            {"code": row[0], "name": row[1], "country": row[2]}
            for row in rows
        ]

    @app.get("/api/flights")
    def flights_search(origin: str, destination: str, date: str, passengers: int = 1):
        if passengers < 1:
            return JSONResponse(status_code=400, content={
                "code": "validation_error",
                "message": "passengers must be at least 1"
            })

        try:
            moscow_tz = ZoneInfo("Europe/Moscow")
            local_start = datetime.strptime(date, "%Y-%m-%d").replace(tzinfo=moscow_tz)
            
            local_end = local_start + timedelta(days=1)
            
            utc_start = local_start.astimezone(ZoneInfo("UTC"))
            utc_end = local_end.astimezone(ZoneInfo("UTC"))
        except (ValueError, TypeError):
            return JSONResponse(status_code=400, content={
                "code": "validation_error",
                "message": "Invalid date format, expected YYYY-MM-DD"
            })

        rows = get_flights(conn, origin, destination,  utc_start, utc_end, passengers)
        
        return [serialize_flight(row) for row in rows]

    @app.get("/api/flights/{flight_id}")
    def flight_by_id(flight_id: str):
        try:
            flight_id_int = int(flight_id)
        except ValueError:
            return JSONResponse(status_code=404, content={
                "code": "not_found",
                "message": f"Flight with id '{flight_id}' not found"
            })

        row = get_flight_by_id(conn, flight_id_int)

        if row is None:
            return JSONResponse(status_code=404, content={
                "code": "not_found",
                "message": f"Flight with id {flight_id_int} not found"
            })

        return serialize_flight(row)

    @app.post("/api/bookings")
    def book(request: CreateBookingRequest):
        if not request.passengers:
                    return JSONResponse(status_code=400, content={
                        "code": "validation_error",
                        "message": "passengers must be at least 1"
                    })
        row = get_flight_by_id(conn, request.flightId)
        if row is None:
            return JSONResponse(status_code=400, content={
                        "code": "not_found",
                        "message": f"Flight with id {request.flightId} not found"
                    })
        total_price = row["price_amount"] * len(request.passengers)
        while True:
            booking_code = generate_booking_code()
            status = "confirmed"
            createdAt = datetime.now(timezone.utc)
            try:
                create_booking(conn, request.flightId, booking_code, total_price, request.contact, request.passengers, status, createdAt)
                break
            except UniqueViolation:
                continue
        return JSONResponse(status_code=201, content=serialize_booking(booking_code, status, row, request.passengers, request.contact, total_price, createdAt))



    @app.get("/{path:path}")
    def spa(path: str):
        PUBLIC_DIR = Path(__file__).resolve().parent.parent / "public"
        file = (PUBLIC_DIR / path).resolve()
        if path and file.is_relative_to(PUBLIC_DIR) and file.is_file():
            return FileResponse(file)
        return FileResponse(PUBLIC_DIR / "index.html")

    return app
