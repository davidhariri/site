import datetime
import uuid
from pydantic import BaseModel, Field
import markdown  # type: ignore
from pymongo import MongoClient
from config import settings


client = MongoClient(settings.MONGODB_URI)
db = client[settings.DATABASE_NAME]
posts_collection = db["posts"]

_now = lambda: datetime.datetime.utcnow()

class Post(BaseModel):
    """
    A blog post, stored in the database.
    """
    id: str
    date_created: datetime.datetime = Field(default_factory=_now)
    date_updated: datetime.datetime = Field(default_factory=_now)
    date_published: datetime.datetime = Field(default_factory=_now)
    title: str
    url_slug: str
    content: str
    description: str | None = None
    tags: set[str] | None = None

    @property
    def html_content(self) -> str:
        return markdown.markdown(self.content, extensions=["fenced_code", "codehilite"])

    @property
    def pretty_date(self) -> str:
        day = self.date_published.day

        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][day % 10 - 1]

        return self.date_published.strftime(f"%A %B %d{suffix}, %Y")

def get_posts() -> list[Post]:
    posts_cursor = posts_collection.find().sort("date_published", -1)
    posts = []
    for post_data in posts_cursor:
        post = Post(
            id=str(post_data["_id"]),
            **post_data,
        )
        posts.append(post)
    return posts


def get_posts_index() -> dict[str, Post]:
    posts = get_posts()
    return {post.url_slug: post for post in posts}

def create_post(title: str, content: str, url_slug: str, tags: set[str] | None = None, description: str | None = None) -> Post:
    """
    Create a new blog post and store it in the database.
    
    Args:
        title (str): The title of the post.
        content (str): The main content of the post.
        url_slug (str): The URL-friendly slug for the post.
        tags (set[str] | None, optional): A set of tags for the post. Defaults to None.
        description (str | None, optional): A brief description of the post. Defaults to None.
    
    Returns:
        Post: The newly created Post object.
    """
    new_post = Post(
        id=str(uuid.uuid4()),
        title=title,
        url_slug=url_slug,
        content=content,
        tags=tags,
        description=description
    )
    
    post_data = new_post.model_dump()
    if post_data['tags']:
        post_data['tags'] = list(post_data['tags'])
    
    result = posts_collection.insert_one(post_data)
    new_post.id = str(result.inserted_id)
    
    return new_post


