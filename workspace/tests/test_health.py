# workspace/tests/test_health.py 
#
# This is a very basic test, but it's a good starting point. You can expand it later with more complex tests as needed.
#
# What it does
# Verifies the API is running and returning expected JSON.
# (Note: TestClient relies on Starlette; FastAPI pulls it in. If you later want async tests with httpx.AsyncClient, you can.)
#
#version 1 - 260210



 
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"ok": True}
