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
from datetime import date, datetime
from rfeed import Feed, Item
from dataclasses import dataclass
import yaml
import copy


@dataclass
class BaseContent:
    title: str
    description: str
    url_slug: str
    date_published: date | None
    raw_content: str
    content: str

    @classmethod
    def from_frontmatter(cls, content: str, url_slug: str, **kwargs):
        data = frontmatter.loads(content)
        date_published = data.metadata.get("date_published")
        
        if isinstance(date_published, str):
            date_published = datetime.fromisoformat(
                date_published.replace("Z", "+00:00")
            )

        md = markdown.Markdown(
            extensions=[
                "fenced_code",
                "codehilite",
                "md_in_html",
                "footnotes",
                "sane_lists",
                "extra",
                "toc",
                "pymdownx.tilde",
            ]
        )
        html_content = md.convert(data.content)

        return cls(
            title=data.metadata.get("title", "Untitled"),
            description=data.metadata.get("description", ""),
            url_slug=url_slug,
            date_published=date_published,
            raw_content=content,
            content=html_content,
            **kwargs,
        )


@dataclass
class Post(BaseContent):
    tags: list[str]


@dataclass
class Page(BaseContent):
    date_last_updated: date | None

@dataclass
class SiteConfig:
    site_domain: str | None
    site_language: str = "en-US"
    site_title: str = "My Site"
    site_description: str = "A website built with Rook"


SITE_CONFIG = SiteConfig(**yaml.safe_load(open("site_config.yaml")))

# MARK - Data loading from files

POSTS_BY_YEAR: dict[int, list[Post]] = {}
POSTS_BY_TAG: dict[str, list[Post]] = {}
POSTS_ALL: list[Post] = []
PAGES: list[Page] = []

# Load all posts into ALL_POSTS, and POSTS_BY_YEAR
for root, _, files in os.walk("posts"):
    for file in files:
        if not file.endswith(".md"):
            continue
            
        file_path = os.path.join(root, file)
        
        with open(file_path, "r") as f:
            content = f.read()
            post_data = frontmatter.loads(content)
            
            # Get relative path from posts directory and strip .md extension
            rel_path = os.path.relpath(file_path, "posts")
            url_slug = os.path.splitext(rel_path)[0]
            
            post = Post.from_frontmatter(
                content,
                url_slug=url_slug,
                tags=post_data.metadata.get("tags", [])
            )

            POSTS_ALL.append(post)
            POSTS_BY_YEAR.setdefault(post.date_published.year, []).append(post)
            
            for tag in post.tags:
                POSTS_BY_TAG.setdefault(tag.strip(), []).append(post)

# Load all pages into ALL_PAGES
for page in os.listdir("pages"):
    with open(os.path.join("pages", page), "r") as f:
        content = f.read()
        page_data = frontmatter.loads(content)
        date_last_updated = page_data.metadata.get("date_last_updated")
        url_slug = os.path.splitext(page)[0]
        
        PAGES.append(
            Page.from_frontmatter(
                content, url_slug=url_slug, date_last_updated=date_last_updated
            )
        )

# MARK - Sorting

# sort ALL_TAGS alphabetically
ALL_TAGS = sorted(POSTS_BY_TAG.keys())

# sort ALL_POSTS with most recent posts first
POSTS_ALL.sort(key=lambda x: x.date_published, reverse=True)

# sort posts in each year with most recent posts first
for year, posts in POSTS_BY_YEAR.items():
    posts.sort(
        key=lambda x: x.date_published if x.date_published else datetime.min,
        reverse=True,
    )

# MARK - Helper functions

def setup_jinja():
    """Set up and return Jinja environment"""
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader("templates"), autoescape=True
    )
    env.globals["config"] = SITE_CONFIG
    env.globals["pages"] = PAGES
    return env


def ensure_dir(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)

# MARK - Compilation Steps

def compile_index():
    """
    Compile the index page into HTML files.
    """
    env = setup_jinja()
    template = env.get_template("index.jinja")
    rendered = template.render(posts=POSTS_ALL[:3])

    with open(os.path.join("public", "index.html"), "w") as f:
        f.write(rendered)


def compile_pages():
    """
    Compile the pages into HTML files.
    """
    env = setup_jinja()
    page_template = env.get_template("page.jinja")

    for page in PAGES:
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

    for year, posts in POSTS_BY_YEAR.items():
        for post in posts:
            # Get year from post date and create year directory
            year_dir = os.path.join("public", str(year))
            ensure_dir(year_dir)

            # Convert .md extension to .html
            html_filename = os.path.splitext(post.url_slug)[0] + ".html"

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
    template = env.get_template("blog_index.jinja")

    with open(os.path.join("public", "blog.html"), "w") as f:
        years = sorted(POSTS_BY_YEAR.keys(), reverse=True)
        f.write(template.render(years=years, posts=POSTS_BY_YEAR, tags=ALL_TAGS))


def compile_tagged_posts():
    """
    Compile the posts into tagged folders like /tagged/programming/index.html which lists all posts tagged with "programming"
    """
    env = setup_jinja()
    template = env.get_template("blog_tagged.jinja")
    
    # Then compile the tagged posts
    for tag in ALL_TAGS:
        # Create the tagged directory if it doesn't exist
        tag_dir = os.path.join("public", "tagged")
        ensure_dir(tag_dir)

        # Get posts for this tag from POSTS_BY_TAG
        tagged_posts = POSTS_BY_TAG[tag]

        with open(os.path.join(tag_dir, f"{tag}.html"), "w") as f:
            f.write(template.render(posts=tagged_posts, tagged=tag))


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
        language=SITE_CONFIG.site_language,
        lastBuildDate=datetime.combine(POSTS_ALL[0].date_published, datetime.min.time()) if POSTS_ALL else datetime.now(),
        items=[],
    )

    for post in POSTS_ALL:
        feed.items.append(
            Item(
                title=post.title,
                link=f"https://{SITE_CONFIG.site_domain}/{post.url_slug}",
                description=post.description,
                pubDate=datetime.combine(post.date_published, datetime.min.time()),
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
    ensure_dir("public")
    compile_index()
    compile_blog_index()
    compile_pages()
    compile_posts()
    compile_tagged_posts()
    compile_404()
    copy_static_files()

    if SITE_CONFIG.site_domain is None:
        print("⏭️ No site_domain in SiteConfig. Skipping RSS Generation.")
    else:
        compile_rss()


if __name__ == "__main__":
    compile_site()
