import datetime
import uuid
from pydantic import BaseModel, Field
import markdown  # type: ignore
from pymongo import MongoClient
from slugify import slugify
from config import settings
import openai

client = MongoClient(settings.MONGODB_URI)
db = client[settings.DATABASE_NAME]
posts_collection = db["posts"]

_now = lambda: datetime.datetime.now(datetime.UTC)

class Post(BaseModel):
    """
    A blog post, stored in the database.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    date_created: datetime.datetime = Field(default_factory=_now)
    date_updated: datetime.datetime = Field(default_factory=_now)
    date_published: datetime.datetime = Field(default_factory=_now)
    title: str
    url_slug: str
    content: str
    description: str | None = None
    tags: list[str] | None = None

    @property
    def html_content(self) -> str:
        return markdown.markdown(
            self.content,
            extensions=["fenced_code", "codehilite", "md_in_html", "footnotes", "sane_lists"]
        )

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
        post_data['id'] = str(post_data["_id"])
        post = Post(**post_data)
        posts.append(post)
    return posts


def get_posts_index() -> dict[str, Post]:
    posts = get_posts()
    return {post.url_slug: post for post in posts}


def create_post(title: str, content: str, tags: list[str] | None = None, description: str | None = None, url_slug: str | None = None) -> Post:
    if url_slug is None:
        url_slug = slugify(title)
    
    # Strip out the first element if it is an h1
    content = content.strip()
    if content.startswith('# '):
        content = content[content.find('\n') + 1:].strip()
    
    # Extract hashtags and add them to tags
    hashtags = {word[1:] for word in content.split() if word.startswith('#')}
    tags = list(set(tags or []) | hashtags)
    
    if not description and settings.OPENAI_API_KEY:        
        openai.api_key = settings.OPENAI_API_KEY
        response = openai.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that replies with short, personal descriptions for blog posts. The user will provide the content in <content> tags. Keep it short, casual, first-person, and in the tone of voice of the user. For example: 'Quick notes on my interview on the Hard Part Interview podcast.' or 'I made a thing that converts your pocket saves into an rss feed'. Reply *only* with the description text and nothing else (no wrapping quotes, <description> tag etc.)."
                },
                {
                    "role": "user",
                    "content": f"""<content>
{content}
</content>"""
                }
            ],
            model="gpt-4o-mini",
        )
        description = response.choices[0].message.content
    
    existing_post = posts_collection.find_one({"url_slug": url_slug})
    
    if existing_post:
        posts_collection.update_one(
            {"url_slug": url_slug},
            {"$set": {
                "title": title,
                "content": content,
                "tags": tags,
                "description": description,
                "date_updated": _now()
            }}
        )
        updated_post = posts_collection.find_one({"url_slug": url_slug})
        return Post(**updated_post)
    else:
        new_post = Post(
            title=title,
            content=content,
            url_slug=url_slug,
            tags=tags,
            description=description
        )
        
        post_data = new_post.model_dump()
        posts_collection.insert_one(post_data)
        
        return new_post

def delete_post(url_slug: str) -> None:
    posts_collection.delete_one({"url_slug": url_slug})
