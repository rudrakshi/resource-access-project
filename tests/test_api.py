from fastapi.testclient import TestClient
from api.resource_api import api

client = TestClient(api)

def test_read_all_resources():
    print(client)
    response = client.get('/resources')
    assert response.status_code == 200
    assert len(response.json()) != 0

def test_read_resource():
    response = client.get('/resources/1001')
    print(response)
    assert response.status_code == 200
    assert len(response.json()) != 0

def test_read_invalid_resource():
    response = client.get('/resources/1010')
    assert response.status_code == 404
    assert len(response.json()) != 0

def test_create_resource():
    body = {"id":1010,"name":"copper","type":"Metal","is_endangered":False}
    response = client.post('/resources/1010', json=body)    
    assert response.status_code == 201
    assert response.json() == {"id":1010,"name":"copper","type":"Metal","is_endangered":False}

def test_create_invalid_resource():
    body = {"id":"copperId","name":"copper","type":"Metal","is_endangered":"Why"}
    response = client.post('/resources/1010', json=body)    
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
            "type": "int_parsing",
            "loc": [
                "body",
                "id"
            ],
            "msg": "Input should be a valid integer, unable to parse string as an integer",
            "input": "copperId",
            "url": "https://errors.pydantic.dev/2.3/v/int_parsing"
            },
            {
            "type": "bool_parsing",
            "loc": [
                "body",
                "is_endangered"
            ],
            "msg": "Input should be a valid boolean, unable to interpret input",
            "input": "Why",
            "url": "https://errors.pydantic.dev/2.3/v/bool_parsing"
            }
        ]
        }

def test_update_resource():
    body = {"id":1010,"name":"iron","type":"Metal","is_endangered":False}
    response = client.put('/resources/1010', json=body)    
    assert response.status_code == 200
    assert response.json() == {"id":1010,"name":"iron","type":"Metal","is_endangered":False}

def test_update_invalid_resource():
    body = {"id":1111,"name":"iron","type":"Metal","is_endangered":False}
    response = client.put('/resources/1111', json=body)    
    assert response.status_code == 404
    assert response.json() == {"detail": "Resource does not exist."}

def test_update_different_resource():
    body = {"id":1010,"name":"iron","type":"Metal","is_endangered":False}
    response = client.put('/resources/1111', json=body)    
    assert response.status_code == 400
    assert response.json() == {"detail": "Path Resource id does not match with content resource id."}

def test_delete_resource():
    response = client.delete('/resources/1010')
    assert response.status_code == 204
    assert not hasattr(response, 'data')

def test_delete_resource_twice():
    response = client.delete('/resources/1010')
    assert response.status_code == 404
    assert response.json() == {"detail": "Resource does not exist."}
