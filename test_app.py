from datetime import datetime
import pytest
from app import app
from service.post import get_posts, create_post, delete_post
from config import settings
from quart.testing import QuartClient

@pytest.fixture(scope="module", autouse=True)
async def insert_fake_post():
    await create_post(title="Fake Post", content="# Test Title\n\nThis is a fake post for testing.\n\nmy content\n\nmy other content", url_slug="fake-post")
    yield
    await delete_post("fake-post")

@pytest.mark.asyncio
async def test_home():
    test_client = app.test_client()
    response = await test_client.get("/")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_404():
    test_client = app.test_client()
    response = await test_client.get("/does-not-exist/")
    data = await response.get_data()
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_blog_index():
    async with app.test_client() as test_client:
        response = await test_client.get("/blog/")
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_post_now_date():
    async with app.test_client() as test_client:
        posts = await get_posts()
        assert isinstance(posts[0].date_updated, datetime)

@pytest.mark.asyncio
async def test_single_post():
    async with app.test_client() as test_client:
        response = await test_client.get("/blog/fake-post/")
        data = await response.get_data()
        assert response.status_code == 200
        assert b"Fake Post" in data
        assert b"This is a fake post for testing." in data

@pytest.mark.asyncio
async def test_micropub_get():
    async with app.test_client() as test_client:
        headers = {
            "Content-Type": "application/json"
        }
        response = await test_client.get("/micropub", headers=headers)
        data = await response.get_json()
        assert response.status_code == 200
        assert "actions" in data
        assert "types" in data
        assert "syndicate-to" in data

@pytest.mark.asyncio
async def test_micropub_post():
    async with app.test_client() as test_client:
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
        response = await test_client.post("/micropub", headers=headers, json=data)
        assert response.status_code == 201
        response_data = await response.get_json()
        assert "url" in response_data
        assert response.headers["Location"] == response_data["url"]

@pytest.mark.asyncio
async def test_micropub_post_invalid_token():
    async with app.test_client() as test_client:
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
        response = await test_client.post("/micropub", headers=headers, json=data)
        assert response.status_code == 401

@pytest.mark.asyncio
async def test_micropub_post_missing_content():
    async with app.test_client() as test_client:
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
        response = await test_client.post("/micropub", headers=headers, json=data)
        data = await response.get_data()
        assert response.status_code == 400
        assert b"Missing content." in data

@pytest.mark.asyncio
async def test_micropub_post_content_with_new_lines():
    async with app.test_client() as test_client:
        post_url = f"{settings.FQD}/blog/fake-post/"
        response = await test_client.get(post_url)
        data = await response.get_data()
        assert response.status_code == 200
        assert b"<p>my content</p>" in data
        assert b"<p>my other content</p>" in data
        assert b"<br>" not in data