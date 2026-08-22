from app import app

client = app.test_client()


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["application"] == "Vedic Horoscope API"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_horoscope():
    response = client.post(
        "/horoscope",
        json={
            "name": "Sachin",
            "date_of_birth": "1995-05-15",
            "time_of_birth": "10:30",
            "place_of_birth": "Pune, India"
        }
    )

    assert response.status_code == 200
    assert response.json["name"] == "Sachin"
    assert "horoscope" in response.json


def test_horoscope_missing_input():
    response = client.post(
        "/horoscope",
        json={
            "name": "Sachin"
        }
    )

    assert response.status_code == 400