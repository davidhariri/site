from datetime import datetime
import pytest
from app import app
from service.post import get_posts, create_post, delete_post
from config import settings

@pytest.fixture(scope="module", autouse=True)
def insert_fake_post():
    create_post(title="Fake Post", content="# Test Title\n\nThis is a fake post for testing.\n\nmy content\n\nmy other content", url_slug="fake-post")
    yield
    delete_post("fake-post")

def test_home():
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200

def test_404():
    with app.test_client() as client:
        response = client.get("/does-not-exist/")
        assert response.status_code == 404

def test_blog_index():
    with app.test_client() as client:
        response = client.get("/blog/")
        assert response.status_code == 200

def test_post_now_date():
    with app.test_client() as client:
        posts = get_posts()
        assert isinstance(posts[0].date_updated, datetime)

def test_single_post():
    with app.test_client() as client:
        response = client.get("/blog/fake-post/")
        assert response.status_code == 200
        assert b"Fake Post" in response.data
        assert b"This is a fake post for testing." in response.data

def test_micropub_get():
    with app.test_client() as client:
        response = client.get("/micropub")
        assert response.status_code == 200
        data = response.get_json()
        assert "actions" in data
        assert "types" in data
        assert "syndicate-to" in data

def test_micropub_post():
    with app.test_client() as client:
        headers = {
            "Authorization": f"Bearer {settings.MICROPUB_SECRET}",
            "Content-Type": "application/json"
        }
        data = {
            "type": ["h-entry"],
            "properties": {
                "content": ["Micropub test content"],
                "name": ["Micropub Test Post"],
                "category": ["test", "micropub"],
                "summary": ["This is a summary for the micropub test post."]
            }
        }
        response = client.post("/micropub", headers=headers, json=data)
        assert response.status_code == 201
        response_data = response.get_json()
        assert "url" in response_data
        assert response.headers["Location"] == response_data["url"]

def test_micropub_post_invalid_token():
    with app.test_client() as client:
        headers = {
            "Authorization": "Bearer invalid_token",
            "Content-Type": "application/json"
        }
        data = {
            "type": ["h-entry"],
            "properties": {
                "content": ["Micropub test content"],
                "name": ["Micropub Test Post"],
                "category": ["test", "micropub"],
                "summary": ["This is a summary for the micropub test post."]
            }
        }
        response = client.post("/micropub", headers=headers, json=data)
        assert response.status_code == 401

def test_micropub_post_missing_content():
    with app.test_client() as client:
        headers = {
            "Authorization": f"Bearer {settings.MICROPUB_SECRET}",
            "Content-Type": "application/json"
        }
        data = {
            "type": ["h-entry"],
            "properties": {
                "name": ["Micropub Test Post"],
                "category": ["test", "micropub"],
                "summary": ["This is a summary for the micropub test post."]
            }
        }
        response = client.post("/micropub", headers=headers, json=data)
        assert response.status_code == 400
        assert b"Missing content." in response.data

def test_micropub_post_content_with_new_lines():
    with app.test_client() as client:
        # Fetch the already created fake-post and check the content rendering
        post_url = f"{settings.FQD}/blog/fake-post/"
        response = client.get(post_url)
        assert response.status_code == 200
        assert b"<p>my content</p>" in response.data
        assert b"<p>my other content</p>" in response.data
        assert b"<br>" not in response.data