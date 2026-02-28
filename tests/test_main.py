import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_export_logic_response():
    # We test that the endpoint returns a valid JSON structure 
    # regardless of whether data was found or not
    response = client.post("/export/test_consumer_unit_test")
    assert response.status_code == 200
    data = response.json()
    
    # Check if it returned a success OR a 'no data' message
    if "status" in data:
        assert data["status"] == "success"
        assert "file" in data
    else:
        assert "message" in data
        assert data["message"] == "No new data to export"