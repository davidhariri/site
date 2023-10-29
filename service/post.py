import os
import datetime
from pydantic import BaseModel, Field
import markdown # type: ignore
import frontmatter

POSTS_DIRECTORY = "./posts"

_now = lambda: datetime.datetime.now(datetime.UTC)

class Post(BaseModel):
    """
    A blog post, stored in the database.
    """
    id: int | None
    date_created: datetime.datetime = Field(default_factory=_now)
    date_updated: datetime.datetime = Field(default_factory=_now)
    date_published: datetime.datetime = Field(default_factory=_now)
    title: str
    url_slug: str
    content: str
    description: str | None
    tags: set[str] | None

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

def __build_posts_dict() -> dict[str, Post]:
    posts_dict = {}
    post_files = [f for f in os.listdir(POSTS_DIRECTORY) if os.path.isfile(os.path.join(POSTS_DIRECTORY, f))]

    for post_file in post_files:
        with open(os.path.join(POSTS_DIRECTORY, post_file), 'r', encoding='utf-8') as f:
            file_content = f.read()
            # Use python-frontmatter to load the file's frontmatter and content
            post_metadata = frontmatter.loads(file_content)
            
            try:
                post_tags = set(post_metadata.get('tags', []))
            except:
                post_tags = set()

            post = Post(
                id=None,
                title=post_metadata.get("title"),
                url_slug=post_file[:-3],
                content=post_metadata.content,
                description=post_metadata.get("description"),
                tags=post_tags,
                date_published=post_metadata.get('date'),
            )
            posts_dict[post.url_slug] = post
    
    return posts_dict

ALL_POSTS = __build_posts_dict()

def get_all_posts() -> list[Post]:
    posts = list(ALL_POSTS.values())
    posts.sort(key=lambda p: p.date_published, reverse=True)
    return posts
