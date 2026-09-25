from fastapi.testclient import TestClient

from ..main import create_app


def test_health():
    app = create_app()
    client = TestClient(app)
    response = client.get("/api/health")
    assert response.status_code == 200 and response.json() == {"status": "ok"} 