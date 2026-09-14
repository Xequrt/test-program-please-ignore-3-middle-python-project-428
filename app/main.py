from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from db import get_connection

def create_app() -> FastAPI:
    app = FastAPI()

    create_conn = get_connection()

    @app.get("/api/health")
    def get_health():
        try:
            with create_conn.cursor() as cur:
                cur.execute("SELECT 1")
                return {"status": "ok", "db": "connected"}
        except Exception as e:
            return {"status": "error", "db": str(e)}
    
    @app.get("/api/cities")
    def get_cities():
        with create_conn.cursor() as cur:
            cur.execute("SELECT code, name, country FROM cities ORDER BY name")
            rows = cur.fetchall()
            
        cities = [
            {"code": row[0], "name": row[1], "country": row[2]}
            for row in rows
        ]
        return cities
    
    @app.get("/{path:path}")
    def spa(path: str):
        PUBLIC_DIR = Path(__file__).resolve().parent.parent / "public"
        
        file = (PUBLIC_DIR / path).resolve()
        if path and file.is_relative_to(PUBLIC_DIR) and file.is_file():
            return FileResponse(file)

        return FileResponse(PUBLIC_DIR / "index.html")

    return app
