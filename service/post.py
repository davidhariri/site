import os
from datetime import datetime
import markdown # type: ignore
from pydantic import BaseModel, Field, validator
import requests
import html2text # type: ignore

from service.config import SUPABASE_URL, SUPBASE_KEY

class Post(BaseModel):
    """
    A blog post, stored in the database.
    """
    id: int | None
    date_created: datetime = Field(default_factory=datetime.utcnow)
    date_updated: datetime = Field(default_factory=datetime.utcnow)
    date_published: datetime = Field(default_factory=datetime.utcnow)
    title: str
    url_slug: str
    content: str
    description: str | None
    tags: set[str] | None
    is_hidden: bool | None = False

    @validator("is_hidden")
    def must_be_hidden_or_not_hidden(cls, v):
        if v == None:
            return False
        return v

    @property
    def html_content(self) -> str:
        return markdown.markdown(self.content)
    
    @property
    def pretty_date(self) -> str:
        day = self.date_published.day

        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][day % 10 - 1]
        
        return self.date_published.strftime(f"%A %B %d{suffix}, %Y")


class PostCreateRequest(BaseModel):
    content: str
    title: str
    url_slug: str | None
    description: str | None
    date_published: datetime | None
    tags: list[str] | None
    is_hidden: bool | None

    @validator("description")
    def must_have_description(cls, v, values):
        if v is None:
            v = values["content"].splitlines()[0]
        return v


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


    def save(self) -> str:
        """
        Save the post to the database and return the url_slug
        """
        self.generate_preview_fields()
        post = Post(**self.dict())
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/posts",
            data=post.json(),
            headers={"apikey": SUPBASE_KEY, "Content-Type": "application/json"},
        )
        response.raise_for_status()
        return post.url_slug


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

