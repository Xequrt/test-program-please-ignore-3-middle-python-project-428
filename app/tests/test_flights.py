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


def test_create_booking_success():
    r = client.post("/api/bookings", json={
        "flightId": "1",
        "contact": {
            "email": "test@example.com",
            "phone": "+79991234567"
        },
        "passengers": [
            {
                "firstName": "Иван",
                "lastName": "Петров",
                "dateOfBirth": "1990-05-20",
                "documentNumber": "4509 123456"
            }
        ]
    })
    assert r.status_code == 201
    data = r.json()
    assert "code" in data
    assert len(data["code"]) == 6
    assert data["status"] == "confirmed"
    assert "totalPrice" in data
    assert data["totalPrice"]["currency"] == "RUB"
    assert "createdAt" in data
    assert len(data["passengers"]) == 1


def test_create_booking_two_passengers():
    flight_r = client.get("/api/flights/1")
    assert flight_r.status_code == 200
    flight = flight_r.json()
    single_price = flight["price"]["amount"]
    
    r = client.post("/api/bookings", json={
        "flightId": "1",
        "contact": {
            "email": "test@example.com",
            "phone": "+79991234567"
        },
        "passengers": [
            {
                "firstName": "Иван",
                "lastName": "Петров",
                "dateOfBirth": "1990-05-20",
                "documentNumber": "1"
            },
            {
                "firstName": "Мария",
                "lastName": "Петрова",
                "dateOfBirth": "1992-03-15",
                "documentNumber": "2"
            }
        ]
    })
    assert r.status_code == 201
    data = r.json()
    assert data["totalPrice"]["amount"] == single_price * 2
    assert len(data["passengers"]) == 2


def test_create_booking_empty_passengers():
    r = client.post("/api/bookings", json={
        "flightId": "1",
        "contact": {
            "email": "test@example.com",
            "phone": "+79991234567"
        },
        "passengers": []
    })
    assert r.status_code == 400
    data = r.json()
    assert data["code"] == "validation_error"


def test_create_booking_missing_field():
    r = client.post("/api/bookings", json={
        "flightId": "1",
        "contact": {
            "email": "test@example.com",
            "phone": "+79991234567"
        }
    })
    assert r.status_code == 400
    data = r.json()
    assert data["code"] == "validation_error"


def test_create_booking_unknown_flight():
    r = client.post("/api/bookings", json={
        "flightId": "999999",
        "contact": {
            "email": "test@example.com",
            "phone": "+79991234567"
        },
        "passengers": [
            {
                "firstName": "Иван",
                "lastName": "Петров",
                "dateOfBirth": "1990-05-20",
                "documentNumber": "1"
            }
        ]
    })
    assert r.status_code == 400
    data = r.json()
    assert data["code"] == "not_found"


def test_create_booking_minimal_document():
    r = client.post("/api/bookings", json={
        "flightId": "1",
        "contact": {
            "email": "a@b.c",
            "phone": "1"
        },
        "passengers": [
            {
                "firstName": "A",
                "lastName": "B",
                "dateOfBirth": "2000-01-01",
                "documentNumber": "1"
            }
        ]
    })
    assert r.status_code == 201


def test_view_booking_success():
    create_r = client.post("/api/bookings", json={
        "flightId": "1",
        "contact": {"email": "test@example.com", "phone": "+79991234567"},
        "passengers": [
            {"firstName": "Иван", "lastName": "Петров", "dateOfBirth": "1990-05-20", "documentNumber": "1"}
        ]
    })
    assert create_r.status_code == 201
    booking_code = create_r.json()["code"]
    
    r = client.get(f"/api/bookings/{booking_code}", params={"lastName": "Петров"})
    assert r.status_code == 200
    data = r.json()
    assert data["code"] == booking_code
    assert data["status"] == "confirmed"


def test_view_booking_case_insensitive():
    create_r = client.post("/api/bookings", json={
        "flightId": "1",
        "contact": {"email": "test@example.com", "phone": "+79991234567"},
        "passengers": [
            {"firstName": "Мария", "lastName": "Иванова", "dateOfBirth": "1992-03-15", "documentNumber": "2"}
        ]
    })
    assert create_r.status_code == 201
    booking_code = create_r.json()["code"]
    
    r = client.get(f"/api/bookings/{booking_code}", params={"lastName": "иванова"})
    assert r.status_code == 200
    
    r = client.get(f"/api/bookings/{booking_code}", params={"lastName": "ИВАНОВА"})
    assert r.status_code == 200


def test_view_booking_wrong_lastname():
    create_r = client.post("/api/bookings", json={
        "flightId": "1",
        "contact": {"email": "test@example.com", "phone": "+79991234567"},
        "passengers": [
            {"firstName": "Пётр", "lastName": "Сидоров", "dateOfBirth": "1985-07-10", "documentNumber": "3"}
        ]
    })
    assert create_r.status_code == 201
    booking_code = create_r.json()["code"]
    
    r = client.get(f"/api/bookings/{booking_code}", params={"lastName": "НеверноеИмя"})
    assert r.status_code == 404
    assert r.json()["code"] == "not_found"


def test_view_booking_missing_lastname():
    r = client.get("/api/bookings/ABC123")
    assert r.status_code == 404
    assert r.json()["code"] == "not_found"


def test_cancel_booking_success():
    create_r = client.post("/api/bookings", json={
        "flightId": "1",
        "contact": {"email": "test@example.com", "phone": "+79991234567"},
        "passengers": [
            {"firstName": "Анна", "lastName": "Кузнецова", "dateOfBirth": "1995-11-25", "documentNumber": "4"}
        ]
    })
    assert create_r.status_code == 201
    booking_code = create_r.json()["code"]
    
    r = client.post(f"/api/bookings/{booking_code}/cancel", json={"lastName": "Кузнецова"})
    assert r.status_code == 200
    data = r.json()
    assert data["code"] == booking_code
    assert data["status"] == "cancelled"


def test_cancel_booking_twice():
    create_r = client.post("/api/bookings", json={
        "flightId": "1",
        "contact": {"email": "test@example.com", "phone": "+79991234567"},
        "passengers": [
            {"firstName": "Олег", "lastName": "Смирнов", "dateOfBirth": "1988-02-14", "documentNumber": "5"}
        ]
    })
    assert create_r.status_code == 201
    booking_code = create_r.json()["code"]
    
    r1 = client.post(f"/api/bookings/{booking_code}/cancel", json={"lastName": "Смирнов"})
    assert r1.status_code == 200
    assert r1.json()["status"] == "cancelled"
    
    r2 = client.post(f"/api/bookings/{booking_code}/cancel", json={"lastName": "Смирнов"})
    assert r2.status_code == 200
    assert r2.json()["status"] == "cancelled"


def test_cancel_booking_missing_lastname():
    r = client.post("/api/bookings/ABC123/cancel", json={"lastName": ""})
    assert r.status_code == 404
    assert r.json()["code"] == "not_found"


def test_cancel_booking_wrong_lastname():
    create_r = client.post("/api/bookings", json={
        "flightId": "1",
        "contact": {"email": "test@example.com", "phone": "+79991234567"},
        "passengers": [
            {"firstName": "Елена", "lastName": "Волкова", "dateOfBirth": "1993-09-05", "documentNumber": "6"}
        ]
    })
    assert create_r.status_code == 201
    booking_code = create_r.json()["code"]
    
    r = client.post(f"/api/bookings/{booking_code}/cancel", json={"lastName": "НеТотЧеловек"})
    assert r.status_code == 404
    assert r.json()["code"] == "not_found"
