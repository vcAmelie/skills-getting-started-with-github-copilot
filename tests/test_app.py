import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    # basic smoke check
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "test_user@example.com"

    # Ensure clean state: remove email if present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    res = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert res.status_code == 200
    body = res.json()
    assert "Signed up" in body.get("message", "")
    assert email in activities[activity]["participants"]

    # Duplicate signup should return 400
    res_dup = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert res_dup.status_code == 400

    # Unregister
    res_un = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert res_un.status_code == 200
    body_un = res_un.json()
    assert "Unregistered" in body_un.get("message", "")
    assert email not in activities[activity]["participants"]

    # Unregistering again should return 404
    res_un2 = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert res_un2.status_code == 404
