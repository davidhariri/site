"""
Author: David Hariri
Date: 2025-02-17

This is a static site generator for my website. It reads posts and pages from /posts and /pages and builds the site in /public.
"""

import os
import shutil
import markdown
import frontmatter
import jinja2
from datetime import datetime
from rfeed import Feed, Item
from dataclasses import dataclass
import yaml
import copy

@dataclass
class Attrs:
    title: str
    description: str
    url_slug: str
    date_published: datetime | None
    content: str

@dataclass
class Post(Attrs):
    tags: list[str]

@dataclass
class Page(Attrs):
    date_last_updated: datetime | None


@dataclass
class PostList:
    year: int
    posts: list[Post]

@dataclass
class SiteConfig:
    site_title: str
    site_description: str
    site_domain: str


MARKDOWN_EXTENSIONS = [
    "fenced_code",
    "codehilite",
    "md_in_html",
    "footnotes",
    "sane_lists",
    "extra",
    "toc",
    "pymdownx.tilde",
]

SITE_CONFIG = SiteConfig(**yaml.load(open("site_config.yaml"), Loader=yaml.SafeLoader))

ALL_POSTS: list[PostList] = []
ALL_PAGES: list[Page] = []

# Load all posts into ALL_POSTS
for year in os.listdir("posts"):
    posts = []
    for post in os.listdir(os.path.join("posts", year)):
        with open(os.path.join("posts", year, post), "r") as f:
            content = f.read()
            post_data = frontmatter.loads(content)
            date_published = post_data.metadata.get('date_published')
            if isinstance(date_published, str):
                date_published = datetime.fromisoformat(date_published.replace('Z', '+00:00'))
            posts.append(
                Post(
                    title=post_data.metadata.get('title', 'Untitled'),
                    description=post_data.metadata.get('description', ''),
                    url_slug=f"{year}/{os.path.splitext(post)[0]}",
                    date_published=date_published,
                    tags=post_data.metadata.get('tags', []),
                    content=post_data.content,
                )
            )
    ALL_POSTS.append(PostList(year=int(year), posts=posts))

# Load all pages into ALL_PAGES
for page in os.listdir("pages"):
    with open(os.path.join("pages", page), "r") as f:
        content = f.read()
        page_data = frontmatter.loads(content)
        date_published = page_data.metadata.get('date_published')
        date_last_updated = page_data.metadata.get('date_last_updated')
        if isinstance(date_published, str):
            date_published = datetime.fromisoformat(date_published.replace('Z', '+00:00'))
        if isinstance(date_last_updated, str):
            date_last_updated = datetime.fromisoformat(date_last_updated.replace('Z', '+00:00'))
        ALL_PAGES.append(
            Page(
                title=page_data.metadata.get('title', 'Untitled'),
                description=page_data.metadata.get('description', ''),
                url_slug=os.path.splitext(page)[0],
                date_published=date_published,
                date_last_updated=date_last_updated,
                content=page_data.content,
            )
        )

ALL_TAGS = set()

for year in ALL_POSTS:
    for post in year.posts:
        ALL_TAGS.update(post.tags)

# sort ALL_TAGS alphabetically
ALL_TAGS = sorted(ALL_TAGS)

# sort ALL_POSTS with most recent posts first
ALL_POSTS.sort(key=lambda x: x.year, reverse=True)

for year in ALL_POSTS:
    year.posts.sort(key=lambda x: x.date_published, reverse=True)

def setup_jinja():
    """Set up and return Jinja environment"""
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"), autoescape=True)
    env.globals["config"] = SITE_CONFIG
    env.globals["pages"] = ALL_PAGES
    return env


def ensure_dir(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)


def compile_index():
    """
    Compile the index page into HTML files.
    """
    ensure_dir("public")
    env = setup_jinja()
    template = env.get_template("index.jinja")

    # Get most recent 5 posts across all years
    recent_posts = []
    for year in ALL_POSTS:
        recent_posts.extend(year.posts[:5])
    recent_posts.sort(key=lambda x: x.date_published, reverse=True)
    
    rendered = template.render(
        posts=recent_posts
    )

    with open(os.path.join("public", "index.html"), "w") as f:
        f.write(rendered)


def compile_pages():
    """
    Compile the pages into HTML files.
    """
    ensure_dir("public")
    env = setup_jinja()
    page_template = env.get_template("page.jinja")

    for page in ALL_PAGES:
        # Convert markdown content
        page.content = markdown.markdown(page.content, extensions=MARKDOWN_EXTENSIONS)
        
        # Render template with page data
        html = page_template.render(page=page)

        # Write rendered HTML to file
        with open(os.path.join("public", f"{page.url_slug}.html"), "w") as f:
            f.write(html)


def compile_posts():
    """
    Compile the posts into HTML files.
    """
    env = setup_jinja()
    post_template = env.get_template("post.jinja")

    for year in ALL_POSTS:
        for post in year.posts:
            # Get year from post date and create year directory
            year_dir = os.path.join("public", str(year.year))
            ensure_dir(year_dir)

            # Convert .md extension to .html
            html_filename = os.path.splitext(post.url_slug)[0] + ".html"

            # Convert markdown content
            html_content = markdown.markdown(
                post.content, extensions=MARKDOWN_EXTENSIONS
            )

            post.content = html_content

            # Render template with metadata
            html = post_template.render(
                post=post,
            )

            with open(os.path.join("public", html_filename), "w") as f:
                f.write(html)


def compile_blog_index():
    """
    Compile the blog index page into HTML files.
    """
    env = setup_jinja()
    blog_index_template = env.get_template("blog.jinja")

    with open(os.path.join("public", "blog.html"), "w") as f:
        f.write(blog_index_template.render(posts=ALL_POSTS, tags=ALL_TAGS))


def compile_tagged_posts():
    """
    Compile the posts into tagged folders like /tagged/programming/index.html which lists all posts tagged with "programming"
    """
    env = setup_jinja()
    blog_index_template = env.get_template("blog.jinja")

    # Then compile the tagged posts
    for tag in ALL_TAGS:
        # Create the tagged directory if it doesn't exist
        tag_dir = os.path.join("public", "tagged")
        ensure_dir(tag_dir)

        # Filter posts by tag across all years, discarding empty years
        tagged_years = []
        for year in ALL_POSTS:
            tagged_posts = [post for post in year.posts if tag in post.tags]
            if tagged_posts:
                # Create a copy of the year with filtered posts
                tagged_year = copy.copy(year)
                tagged_year.posts = tagged_posts
                tagged_years.append(tagged_year)

        with open(os.path.join(tag_dir, f"{tag}.html"), "w") as f:
            f.write(blog_index_template.render(posts=tagged_years, tagged=tag))

def copy_static_files():
    """
    Copy static files to the public/static directory.
    """
    # Create public/static directory
    static_dest = os.path.join("public", "static")
    ensure_dir(static_dest)

    for root, dirs, files in os.walk("static"):
        # Get the relative path from static directory
        rel_path = os.path.relpath(root, "static")

        # Create corresponding directory in public/static if it doesn't exist
        dest_dir = os.path.join(static_dest, rel_path)
        ensure_dir(dest_dir)

        # Copy all files in current directory
        for file in files:
            src = os.path.join(root, file)
            dst = os.path.join(dest_dir, file)
            shutil.copy2(src, dst)


def compile_rss():
    """
    Generate RSS feed XML file
    """
    feed = Feed(
        title=SITE_CONFIG.site_title,
        link=f"https://{SITE_CONFIG.site_domain}/blog.html",
        description=SITE_CONFIG.site_description,
        language="en-US",
        lastBuildDate=max(post.date_published for year in ALL_POSTS for post in year.posts),
        items=[],
    )

    for year in ALL_POSTS:
        for post in year.posts:
            feed.items.append(
                Item(
                    title=post.title,
                    link=f"https://{SITE_CONFIG.site_domain}/{post.url_slug}",
                    description=post.description,
                    pubDate=post.date_published,
                )
            )

    with open(os.path.join("public", "rss.xml"), "w") as f:
        f.write(feed.rss())

def compile_404():
    """
    Compile the 404 page into HTML files.
    """
    env = setup_jinja()
    template = env.get_template("404.jinja")
    rendered = template.render()
    
    with open(os.path.join("public", "404.html"), "w") as f:
        f.write(rendered)

def compile_site():
    """
    Compile the site into HTML files.
    """
    ensure_dir("public")  # Ensure public directory exists before any compilation
    compile_index()
    compile_blog_index()
    compile_pages()
    compile_posts()
    compile_tagged_posts()
    compile_rss()
    compile_404()
    copy_static_files()


if __name__ == "__main__":
    compile_site()
