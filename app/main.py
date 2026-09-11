from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse


def create_app() -> FastAPI:
    app = FastAPI()

    @app.get("/api/health")
    def get_health():
        return {"status": "ok"}
    
    @app.get("/api/cities")
    def get_cities():
        return []
    
    @app.get("/{path:path}")
    def spa(path: str):
        PUBLIC_DIR = Path(__file__).resolve().parent.parent / "public"
        
        file = (PUBLIC_DIR / path).resolve()
        if path and file.is_relative_to(PUBLIC_DIR) and file.is_file():
            return FileResponse(file)

        return FileResponse(PUBLIC_DIR / "index.html")

    return app
