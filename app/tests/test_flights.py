from fastapi.testclient import TestClient
from app.main import create_app

client = TestClient(create_app())


def test_search_success():
    r = client.get("/api/flights", params={
        "origin": "MOW", "destination": "LED", "date": "2026-09-17"
    })
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    if data:
        f = data[0]
        assert "id" in f
        assert isinstance(f["origin"], dict)
        assert "code" in f["origin"]


def test_search_empty():
    r = client.get("/api/flights", params={
        "origin": "MOW", "destination": "MOW", "date": "2026-09-17"
    })
    assert r.status_code == 200
    assert r.json() == []


def test_search_missing_date():
    r = client.get("/api/flights", params={
        "origin": "MOW", "destination": "LED"
    })
    assert r.status_code == 400
    assert r.json()["code"] == "validation_error"


def test_search_invalid_date():
    r = client.get("/api/flights", params={
        "origin": "MOW", "destination": "LED", "date": "NOPE"
    })
    assert r.status_code == 400
    assert r.json()["code"] == "validation_error"


def test_search_zero_passengers():
    r = client.get("/api/flights", params={
        "origin": "MOW", "destination": "LED",
        "date": "2026-09-17", "passengers": 0
    })
    assert r.status_code == 400
    assert r.json()["code"] == "validation_error"


def test_flight_by_id():
    r = client.get("/api/flights/1")
    assert r.status_code == 200
    f = r.json()
    assert f["id"] == 1
    assert isinstance(f["origin"], dict)


def test_flight_by_id_not_found():
    r = client.get("/api/flights/999999")
    assert r.status_code == 404
    assert r.json()["code"] == "not_found"


def test_flight_by_id_not_a_number():
    r = client.get("/api/flights/NOPE")
    assert r.status_code == 404
    assert r.json()["code"] == "not_found"
