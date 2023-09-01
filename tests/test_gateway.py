import sys
sys.path.insert(0,'../gateway')
from fastapi.testclient import TestClient
from gateway import *
from gateway.gateway_api import gate


client = TestClient(gate)

def test_unauthentic_read_resources():
    response = client.get('/api/resources')
    assert response.status_code == 401
    assert response.json() == {
            "detail": "Not authenticated"
            }

def test_nonuser_read_token():
    global ACCESS_TOKEN
    response = client.post('/token', params={"username":"test","password":"test"})
    assert response.status_code == 404
    assert response.json() == {
            "detail": "User not found."
            }

def test_wrong_password_token():
    global ACCESS_TOKEN
    response = client.post('/token', params={"username":"johndoe","password":"test"})
    assert response.status_code == 401
    assert response.json() == {
            "detail": "Incorrect username or password"
            }
    
def test_read_token():
    global ACCESS_TOKEN
    response = client.post('/token', params={"username":"johndoe","password":"secret"})
    assert response.status_code == 200
    assert len(response.json()) != 0
    ACCESS_TOKEN = response.json()["access_token"]
    
def test_read_resources():
    response = client.get('/api/resources', headers={"Authorization": "Bearer "+ACCESS_TOKEN})
    assert response.status_code == 200
    assert len(response.json()) != 0

def test_read_with_expired_token():
    response = client.get('/api/resources', headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWJqZWN0IjoiamFuZWRvZSIsImV4dHJhX2luZm8iOiJzaG9ydCBsaXZlZCB0b2tlbiIsInNjb3BlIjpbInJlYWQiLCJ3cml0ZSJdLCJleHAiOjE2OTMxNzA0NjN9.kw31UQVVWoMfuIUWmH3euUSKAtEcqVIV4HyqjbQh2To"})
    assert response.status_code == 400
    assert response.json() == {
            "detail": {"message": "Token expired", "status": "error"}
            }

def test_authorized_read_nonexistence():
    response = client.get('/api/something', headers={"Authorization": "Bearer "+ACCESS_TOKEN})
    assert response.status_code == 404
    assert response.json() == {
            "detail": "Not Found"
            }

def test_unauthorized_create_resources():
    response = client.post('/api/resources', headers={"Authorization": "Bearer "+ACCESS_TOKEN})
    assert response.status_code == 403
    assert response.json() == {
            "detail": "Access is not allowed"
            }

def test_unauthorized_change_resources():
    response = client.put('/api/resources', headers={"Authorization": "Bearer "+ACCESS_TOKEN})
    assert response.status_code == 403
    assert response.json() == {
            "detail": "Access is not allowed"
            }

def test_unauthorized_delete_resources():
    response = client.delete('/api/resources', headers={"Authorization": "Bearer "+ACCESS_TOKEN})
    assert response.status_code == 403
    assert response.json() == {
            "detail": "Access is not allowed"
            }
