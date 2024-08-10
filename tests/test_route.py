"""
Route unit tests
"""

from weather_api import OpenWeatherAPI


def test_health_check(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"health_check": "OK"}


def test_route_not_found(test_client):
    response = test_client.get("/does/not/exists")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_route_get_process(test_client):
    response = test_client.get("/api/v1/process")
    # missing parameters
    assert response.status_code == 422

    response = test_client.get("/api/v1/process", params={"user_id": 0})
    assert response.status_code == 200
    assert response.json() == {
        "user_id": None,
        "total_cities": 0,
        "completed": 0,
        "percentage": 0.0,
        "cities": [],
    }


def test_route_post_process(test_client):
    response = test_client.post("/api/v1/process")
    # missing parameters
    assert response.status_code == 422

    # Creating new process
    user_id = 1
    response = test_client.post(
        "/api/v1/process", json={"user_id": user_id, "cities_id": [3439525]}
    )

    assert response.status_code == 201
    assert response.json() == {
        "user_id": user_id,
    }

    # Duplicated user_id
    response = test_client.post(
        "/api/v1/process", json={"user_id": user_id, "cities_id": [3439525]}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Process already exists"}
    OpenWeatherAPI.queue.clear()
