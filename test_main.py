from fastapi.testclient import TestClient
from main import app


client = TestClient(app=app)

def test_get_all_products():
    response = client.get("/product/all")
    assert response.status_code == 200
    
def test_auth_error():
    response = client.post("/auth/token", data={"username": "", "password": ""})
    access_token = response.json().get("access_token")
    assert access_token is None
    message = response.json().get("detail")[0].get("msg")
    assert message == "Field required"
    
def test_auth_success():
    response = client.post("/auth/token", data={"username": "test", "password": "test"})
    access_token = response.json().get("access_token")
    assert access_token

def test_post_creationg():
    auth = client.post("/auth/token", data={"username": "test", "password": "test"})
    access_token = auth.json().get("access_token")
    assert access_token
    
    response = client.post("/posts/",
                           json={
                               "title": "Test article",
                               "content": "bla bla bla",
                               "published": True,
                               "user_id": 1
                           })
    assert response.status_code == 201
    assert response.json().get("title") == "Test article"