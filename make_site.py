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
from urllib.parse import quote
import argparse  # Add argparse for CLI argument parsing
import uuid  # Add UUID for cache busting


@dataclass
class BaseContent:
    title: str
    description: str
    url_slug: str
    date_published: datetime | None
    raw_content: str
    content: str
    tags: list[str] = None
    cover_photo: str | None = None

    @classmethod
    def from_frontmatter(cls, content: str, url_slug: str, **kwargs):
        data = frontmatter.loads(content)
        date_published = data.metadata.get("date_published")
        
        # Ensure date_published is always a datetime object or None
        if date_published is not None:
            if isinstance(date_published, str):
                date_published = datetime.fromisoformat(
                    date_published.replace("Z", "+00:00")
                )
            elif isinstance(date_published, date) and not isinstance(date_published, datetime):
                date_published = datetime.combine(date_published, datetime.min.time())

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
            tags=data.metadata.get("tags", []),
            cover_photo=data.metadata.get("cover_photo", None),
            **kwargs,
        )


@dataclass
class Post(BaseContent):
    pass


@dataclass
class Page(BaseContent):
    date_last_updated: datetime | None = None

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

def load_posts(include_drafts=False):
    """
    Load all posts into POSTS_ALL, POSTS_BY_YEAR, and POSTS_BY_TAG.
    Optionally include drafts if include_drafts is True.
    """
    global POSTS_ALL, POSTS_BY_YEAR, POSTS_BY_TAG
    
    # Reset the post collections to avoid duplicates when reloading
    POSTS_ALL = []
    POSTS_BY_YEAR = {}
    POSTS_BY_TAG = {}
    
    # Directories to load posts from
    directories = ["posts"]
    if include_drafts:
        directories.append("drafts")
    
    for directory in directories:
        if not os.path.exists(directory):
            continue
            
        for root, _, files in os.walk(directory):
            for file in files:
                if not file.endswith(".md"):
                    continue
                    
                file_path = os.path.join(root, file)
                
                with open(file_path, "r") as f:
                    content = f.read()
                    
                    # Get relative path from the source directory and strip .md extension
                    rel_path = os.path.relpath(file_path, directory)
                    url_slug = os.path.splitext(rel_path)[0]
                    try:
                        post = Post.from_frontmatter(
                            content,
                            url_slug=url_slug
                        )
                    except yaml.scanner.ScannerError as e:
                        print(f"Error parsing {file_path}: {e}")
                        continue
                    
                    POSTS_ALL.append(post)
                    
                    if post.date_published:
                        POSTS_BY_YEAR.setdefault(post.date_published.year, []).append(post)
                    
                    if post.tags:
                        for tag in post.tags:
                            POSTS_BY_TAG.setdefault(tag.strip(), []).append(post)

def load_pages():
    """Load all pages into PAGES."""
    global PAGES
    PAGES = []
    
    if not os.path.exists("pages"):
        return
        
    for page in os.listdir("pages"):
        if not page.endswith(".md"):
            continue
            
        with open(os.path.join("pages", page), "r") as f:
            content = f.read()
            page_data = frontmatter.loads(content)
            date_last_updated = page_data.metadata.get("date_last_updated")
            
            # Ensure date_last_updated is a datetime object if it exists
            if date_last_updated is not None:
                if isinstance(date_last_updated, str):
                    date_last_updated = datetime.fromisoformat(
                        date_last_updated.replace("Z", "+00:00")
                    )
                elif isinstance(date_last_updated, date) and not isinstance(date_last_updated, datetime):
                    date_last_updated = datetime.combine(date_last_updated, datetime.min.time())
                    
            url_slug = os.path.splitext(page)[0]
            
            PAGES.append(
                Page.from_frontmatter(
                    content, url_slug=url_slug, date_last_updated=date_last_updated
                )
            )

def sort_posts():
    """Sort posts by date."""
    global ALL_TAGS
    
    # sort ALL_TAGS alphabetically
    ALL_TAGS = sorted(POSTS_BY_TAG.keys())

    # Define a key function that handles None values
    def sort_key(post):
        if post.date_published is None:
            return datetime.min
        return post.date_published

    # sort ALL_POSTS with most recent posts first
    POSTS_ALL.sort(key=sort_key, reverse=True)

    # sort posts in each year with most recent posts first
    for year, posts in POSTS_BY_YEAR.items():
        posts.sort(key=sort_key, reverse=True)

# MARK - Helper functions

def setup_jinja():
    """Set up and return Jinja environment"""
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader("templates"), autoescape=True
    )
    env.globals["config"] = SITE_CONFIG
    env.globals["pages"] = PAGES
    env.globals["cache_bust_id"] = str(uuid.uuid4())
    
    # Add custom filter for ordinal date formatting
    def ordinal_date(dt):
        """Format date with ordinal suffix (1st, 2nd, 3rd, etc.)"""
        day = dt.day
        suffix = ""
        
        if 11 <= day <= 13:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
            
        # Use a more cross-platform compatible approach
        return f"{dt.strftime('%B')} {day}{suffix} {dt.strftime('%Y')}"
    
    env.filters["ordinal_date"] = ordinal_date
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

        # Sort posts by date_published in descending order (newest first)
        tagged_posts.sort(key=lambda post: post.date_published if post.date_published else datetime.min, reverse=True)

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
    # Get the last build date from the most recent post or use current time
    last_build_date = datetime.now()
    if POSTS_ALL:
        # Ensure we're using a datetime object
        if isinstance(POSTS_ALL[0].date_published, datetime):
            last_build_date = POSTS_ALL[0].date_published
        elif isinstance(POSTS_ALL[0].date_published, date):
            last_build_date = datetime.combine(POSTS_ALL[0].date_published, datetime.min.time())
    
    feed = Feed(
        title=SITE_CONFIG.site_title,
        link=f"https://{SITE_CONFIG.site_domain}/blog.html",
        description=SITE_CONFIG.site_description,
        language=SITE_CONFIG.site_language,
        lastBuildDate=last_build_date,
        items=[],
    )

    for post in POSTS_ALL:
        # Ensure we're using a datetime object for pubDate
        pub_date = datetime.now()
        if post.date_published:
            if isinstance(post.date_published, datetime):
                pub_date = post.date_published
            elif isinstance(post.date_published, date):
                pub_date = datetime.combine(post.date_published, datetime.min.time())
                
        feed.items.append(
            Item(
                title=post.title,
                link=f"https://{SITE_CONFIG.site_domain}/{post.url_slug}",
                description=post.description,
                pubDate=pub_date,
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


def compile_sitemap():
    """
    Generate sitemap.xml containing all pages, posts and tag pages
    """
    # Start with the XML declaration and root element
    sitemap = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]

    # Helper function to add a URL to the sitemap
    def add_url(path, date_obj=None):
        # URL encode the path, preserving forward slashes
        encoded_path = '/'.join(quote(segment) for segment in path.split('/'))
        
        url = [f"  <url>"]
        url.append(f"    <loc>https://{SITE_CONFIG.site_domain}/{encoded_path}</loc>")
        if date_obj:
            # Ensure date_obj is a date object for the sitemap
            if isinstance(date_obj, datetime):
                date_str = date_obj.date().isoformat()
            else:
                date_str = date_obj.isoformat()
            url.append(f"    <lastmod>{date_str}</lastmod>")
        url.append("  </url>")
        sitemap.extend(url)

    # Add homepage
    add_url("index.html")

    # Add blog index
    add_url("blog.html")

    # Add all pages
    for page in PAGES:
        last_updated = page.date_last_updated or page.date_published
        add_url(
            f"{page.url_slug}.html",
            last_updated
        )

    # Add all posts
    for post in POSTS_ALL:
        add_url(
            f"{post.url_slug}.html",
            post.date_published
        )

    # Add all tag pages
    for tag in ALL_TAGS:
        add_url(f"tagged/{tag}.html")

    # Close root element
    sitemap.append("</urlset>")

    # Write the sitemap file
    with open(os.path.join("public", "sitemap.xml"), "w") as f:
        f.write("\n".join(sitemap))


def compile_robots():
    """
    Generate robots.txt file to control search engine crawling
    """
    robots_content = [
        f"# robots.txt for {SITE_CONFIG.site_domain or 'this site'}",
        "User-agent: *",
        "Allow: /",
        "",
        "# Sitemap location",
        f"Sitemap: https://{SITE_CONFIG.site_domain}/sitemap.xml",
    ]
    
    # Write the robots.txt file
    with open(os.path.join("public", "robots.txt"), "w") as f:
        f.write("\n".join(robots_content))


def compile_redirects():
    """
    Generate _redirects file for Netlify to handle URL structure changes.
    Redirects posts from /blog/post-name to /<year>/post-name
    for posts published before February 20, 2025.
    """
    # Convert cutoff_date to datetime for consistent comparison
    cutoff_date = datetime(2025, 2, 16)
    redirects = []
    
    for post in POSTS_ALL:
        if post.date_published and post.date_published < cutoff_date:
            # Extract just the filename without year prefix
            filename = os.path.basename(post.url_slug)
            
            # Create redirect from old URL structure to new URL structure
            old_path = f"/blog/{filename}"
            new_path = f"/{post.url_slug}"
            redirects.append(f"{old_path} {new_path} 301")
    
    # Write the redirects file
    with open(os.path.join("public", "_redirects"), "w") as f:
        f.write("\n".join(redirects))


def compile_site(include_drafts=False):
    """Compile the site with optional inclusion of drafts."""
    # Load content
    load_posts(include_drafts)
    load_pages()
    sort_posts()
    
    # Build site
    ensure_dir("public")
    compile_index()
    compile_blog_index()
    compile_pages()
    compile_posts()
    compile_tagged_posts()
    compile_404()
    compile_redirects()
    copy_static_files()

    if SITE_CONFIG.site_domain is None:
        print("No site_domain in SiteConfig. Skipping RSS, Sitemap, and Robots Generation.")
        return
    
    compile_rss()
    compile_sitemap()
    compile_robots()


if __name__ == "__main__":
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Static site generator")
    parser.add_argument("--with-drafts", action="store_true", help="Include drafts in the compiled site")
    args = parser.parse_args()
    
    # Compile the site with or without drafts based on the command line argument
    compile_site(include_drafts=args.with_drafts)
