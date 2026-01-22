import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data
    assert "description" in data["Basketball Team"]

def test_signup_for_activity():
    # Test successful signup
    response = client.post("/activities/Basketball Team/signup?email=test@example.com")
    assert response.status_code == 200
    assert "Signed up test@example.com for Basketball Team" in response.json()["message"]

    # Test duplicate signup
    response = client.post("/activities/Basketball Team/signup?email=test@example.com")
    assert response.status_code == 400
    assert "Student already signed up" in response.json()["detail"]

def test_signup_nonexistent_activity():
    response = client.post("/activities/Nonexistent Activity/signup?email=test@example.com")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_unregister_from_activity():
    # First sign up
    client.post("/activities/Soccer Club/signup?email=test2@example.com")

    # Then unregister
    response = client.request("DELETE", "/activities/Soccer Club/participants?email=test2@example.com")
    assert response.status_code == 200
    assert "Unregistered test2@example.com from Soccer Club" in response.json()["message"]

def test_unregister_not_signed_up():
    response = client.request("DELETE", "/activities/Soccer Club/participants?email=notsigned@example.com")
    assert response.status_code == 400
    assert "Student not signed up for this activity" in response.json()["detail"]

def test_unregister_nonexistent_activity():
    response = client.request("DELETE", "/activities/Nonexistent Activity/participants?email=test@example.com")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]