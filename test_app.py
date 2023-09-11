from app import app

def test_home():
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200

def test_404():
    with app.test_client() as client:
        response = client.get("/does-not-exist/")
        assert response.status_code == 404