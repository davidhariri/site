import os
from datetime import datetime
import markdown # type: ignore
from pydantic import BaseModel
import requests
import html2text # type: ignore

from service.config import SUPABASE_URL, SUPBASE_KEY

class Post(BaseModel):
    """
    A blog post, stored in the database.
    """
    id: int
    date_created: datetime
    date_updated: datetime
    date_published: datetime
    title: str
    url_slug: str
    content: str
    description: str | None
    tags: set[str] | None
    is_hidden: bool

    @property
    def html_content(self) -> str:
        return markdown.markdown(self.content)

class PostCreateRequest(BaseModel):
    content: str
    title: str
    url_slug: str | None
    description: str | None
    date_published: datetime | None
    tags: list[str] | None
    is_hidden: bool | None

    def generate_preview_fields(self):
        html_content = markdown.markdown(self.content)
        handler = html2text.HTML2Text()
        handler.ignore_links = True
        handler.ignore_images = True
        handler.ignore_emphasis = True
        handler.ignore_tables = True
        
        text_content = handler.handle(html_content)
        text_content = text_content.replace("\n> ", "\n")
        
        if self.description is None:
            first_p = text_content.splitlines()[0]

            if len(first_p) > 200:
                self.description = first_p[:200] + "..."
            else:
                self.description = first_p

        if self.url_slug is None:
            self.url_slug = self.title.lower().replace("?", "").replace("!", "").replace(":", "").replace(";", "").replace(",", "").replace(".", "").replace(" ", "-")
        
        if self.date_published is None:
            self.date_published = datetime.utcnow()

    def save(self):
        self.generate_preview_fields()
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/posts",
            data=self.json(),
            headers={"apikey": SUPBASE_KEY, "Content-Type": "application/json"},
        )
        response.raise_for_status()

def get_all_posts() -> list[Post]:
    """
    Get all posts from the database, sorted by date_published in newest-first order.
    """
    posts_data = requests.get(f"{SUPABASE_URL}/rest/v1/posts?is_hidden=is.false", headers={"apikey": SUPBASE_KEY}).json()
    posts = [Post(**p) for p in posts_data]
    posts = sorted(
        posts, key=lambda post: post.date_published, reverse=True
    )
    return posts

def get_single_post(post_url_slug: str) -> Post | None:
    """
    Get a single post from the database, by its URL slug.
    """
    post_data: list[dict] = requests.get(
        f"{SUPABASE_URL}/rest/v1/posts?url_slug=eq.{post_url_slug}",
        headers={"apikey": SUPBASE_KEY}).json()
    
    if not post_data:
        return None

    post = Post(**post_data[0])
    return post

