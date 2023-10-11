import os
from flask import abort, Flask, render_template
from flask_caching import Cache
from rfeed import Item as RSSItem, Feed as RSSFeed  # type: ignore
import sentry_sdk

from service.page import get_all_page_paths_and_pages, get_all_pages_sorted
from service.post import ALL_POSTS, get_all_posts

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

FQD = "https://dhariri.com"

cache = Cache(config={"CACHE_TYPE": "SimpleCache"})
app = Flask(__name__)

cache.init_app(app)


@app.errorhandler(404)
def render_not_found(_):
    return render_template("404.html"), 404


@app.get("/")
@cache.cached(timeout=60)
def render_home():
    latest_posts = get_all_posts()[:3]
    return render_template(
        "home.html", posts=latest_posts, pages=get_all_pages_sorted()
    )


@app.get("/blog/")
@cache.cached(timeout=60)
def render_blog_index():
    return render_template(
        "blog.html", title="Blog", posts=get_all_posts(), pages=get_all_pages_sorted()
    )


@app.get("/blog/<string:post_path>/")
@cache.memoize(timeout=3600)
def render_blog_post(post_path: str):
    try:
        post = ALL_POSTS.get(post_path)
    except KeyError:
        abort(404)

    return render_template("blog_post.html", post=post, pages=get_all_pages_sorted())


@app.get("/feed/")
@app.get("/rss/")
@cache.cached(timeout=60)
def read_feed():
    items = [
        RSSItem(
            title=post.title,
            link=f"{FQD}/blog/{post.url_slug}",
            description=post.description or "",
            pubDate=post.date_published,
        )
        for post in get_all_posts()
    ]
    feed = RSSFeed(
        title="David Hariri",
        link=f"{FQD}/blog/",
        description="The blog of David Hariri. Programming, design, and more.",
        language="en-US",
        lastBuildDate=items[0].pubDate,
        items=items,
    )
    return feed.rss()


@app.get("/<string:page_path>/")
@cache.memoize(timeout=3600)
def render_page(page_path: str):
    try:
        page = get_all_page_paths_and_pages()[page_path]
    except KeyError:
        abort(404)

    return render_template("page.html", page=page, pages=get_all_pages_sorted())
