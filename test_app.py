from datetime import datetime
from app import app
from service.post import get_all_posts

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
        posts = get_all_posts()
        assert isinstance(posts[0].date_updated, datetime)