from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

def test_read_route():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "hello word"}