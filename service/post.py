import datetime
import uuid
from flask import json
from pydantic import BaseModel, Field
import markdown  # type: ignore
from motor.motor_asyncio import AsyncIOMotorClient
import sentry_sdk
from slugify import slugify
from config import settings
import openai
from bs4 import BeautifulSoup

from service.common import MARKDOWN_EXTENSIONS

client = AsyncIOMotorClient(settings.MONGODB_URI)
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
        html = markdown.markdown(
            self.content,
            extensions=MARKDOWN_EXTENSIONS,
        )
        soup = BeautifulSoup(html, 'html.parser')
        
        for img in soup.find_all('img'):
            if img['src'].endswith('.png') or img['src'].endswith('.svg'):
                img['class'] = img.get('class', []) + ['no_frame']
        
        return str(soup)

    @property
    def pretty_date(self) -> str:
        day = self.date_published.day

        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][day % 10 - 1]

        return self.date_published.strftime(f"%A %B %d{suffix}, %Y")

async def get_posts() -> list[Post]:
    posts_cursor = posts_collection.find().sort("date_published", -1)
    posts = []
    async for post_data in posts_cursor:
        post_data['id'] = str(post_data["_id"])
        post = Post(**post_data)
        posts.append(post)
    return posts

async def get_posts_index() -> dict[str, Post]:
    posts = await get_posts()
    return {post.url_slug: post for post in posts}

class PostMetadata(BaseModel):
    description: str
    tags: list[str]

class PostCreateResult(BaseModel):
    post: Post
    updated_existing: bool

async def create_post(title: str, content: str, tags: list[str] | None = None, description: str | None = None, url_slug: str | None = None) -> PostCreateResult:
    if url_slug is None:
        url_slug = slugify(title)
    
    available_tags = ",".join(get_all_tags())
    
    # Strip out the first element if it is an h1
    content = content.strip()
    if content.startswith('# '):
        content = content[content.find('\n') + 1:].strip()
    
    if (description is None or tags is None) and settings.OPENAI_API_KEY:
        try:
            openai.api_key = settings.OPENAI_API_KEY
            response = openai.beta.chat.completions.parse(
                messages=[
                    {
                        "role": "system",
                        "content": f"""You are a helpful assistant that summarizes blog posts by creating an opengraph description and a list of tags. Do not make your descriptions sales-y or inauthentic. Descriptions must be short enough to fit in a tweet. Tags must be from this list: {available_tags}

    Here is an example

    <example>
    <content>
    Clearing out my Pocket saves. I don't remember how I found this, but it's beautiful.

    > There comes a moment in life, often in the quietest of hours, when one realizes that the world will continue on its wayward course, indifferent to our desires or frustrations. And it is then, perhaps, that a subtle truth begins to emerge: the only thing we truly possess, the only thing we might, with enough care, exert some mastery over, is our mind. It is not a realization of resignation, but rather of liberation. For if the mind can be ordered, if it can be made still in the midst of this restless life

    - [The Quiet Art of Attention](https://billwear.github.io/art-of-attention.html)
    </content>

    You:
    {{
        "description": "A contemplative quote about finding stillness and clarity from 'The Quiet Art of Attention'"
        "tags": ["Philosophy", "Quotes"]
    }}
    </example>"""
                    },
                    {
                        "role": "user",
                        "content": f"""<content>
    {content}
    </content>"""
                    }
                ],
                model="gpt-4o",
                response_format=PostMetadata,
            )
            metadata = response.choices[0].message.parsed

            if description is None:
                description = metadata.description
            
            if tags is None:
                tags = metadata.tags

        except openai.AuthenticationError as e:
            sentry_sdk.capture_exception(e)
        
    existing_post = await posts_collection.find_one({"url_slug": url_slug})
    
    if existing_post:
        await posts_collection.update_one(
            {"url_slug": url_slug},
            {"$set": {
                "title": title,
                "content": content,
                "tags": tags,
                "description": description,
                "date_updated": _now()
            }}
        )
        updated_post = await posts_collection.find_one({"url_slug": url_slug})
        return PostCreateResult(post=Post(**updated_post), updated_existing=True)
    else:
        new_post = Post(
            title=title,
            content=content,
            url_slug=url_slug,
            tags=tags,
            description=description
        )
        
        post_data = new_post.model_dump()
        await posts_collection.insert_one(post_data)
        
        return PostCreateResult(post=new_post, updated_existing=False)

async def delete_post(url_slug: str) -> None:
    await posts_collection.delete_one({"url_slug": url_slug})

async def get_all_tags() -> list[str]:
    pipeline = [
        {"$unwind": "$tags"},
        {"$group": {"_id": None, "unique_tags": {"$addToSet": "$tags"}}},
        {"$project": {"_id": 0, "tags": "$unique_tags"}}
    ]
    cursor = posts_collection.aggregate(pipeline)
    result = await cursor.to_list(length=1)
    tags = result[0]["tags"] if result else []
    return sorted(tags, key=str.lower)
