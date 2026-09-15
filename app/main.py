from pathlib import Path
from datetime import datetime
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse

from .db import get_connection
from .sql import get_flights, get_flight_by_id
from .serializers import serialize_flight


def create_app() -> FastAPI:
    app = FastAPI()
    conn = get_connection()

    @app.exception_handler(RequestValidationError)
    def validation_exception_handler(request, exc):
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
            datetime.strptime(date, "%Y-%m-%d")
        except (ValueError, TypeError):
            return JSONResponse(status_code=400, content={
                "code": "validation_error",
                "message": "Invalid date format, expected YYYY-MM-DD"
            })

        rows = get_flights(conn, origin, destination, date, passengers)
        
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

    @app.get("/{path:path}")
    def spa(path: str):
        PUBLIC_DIR = Path(__file__).resolve().parent.parent / "public"
        file = (PUBLIC_DIR / path).resolve()
        if path and file.is_relative_to(PUBLIC_DIR) and file.is_file():
            return FileResponse(file)
        return FileResponse(PUBLIC_DIR / "index.html")

    return app
