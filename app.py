from datetime import datetime
import os
from flask import abort, Flask, render_template, request
from flask_caching import Cache
from requests import HTTPError
from rfeed import Item as RSSItem, Feed as RSSFeed # type: ignore
from flask_pydantic import validate # type: ignore

from service.config import APP_SECRET
from service.page import Page, get_all_page_paths_and_pages, get_all_pages_sorted
from service.post import PostCreateRequest, get_all_posts, get_single_post

FQD = "https://dhariri.com"

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
app = Flask(__name__)

cache.init_app(app)


@app.errorhandler(404)
def render_not_found(_):
    return render_template("404.html"), 404


@app.get("/")
@cache.cached(timeout=60)
def render_home():
    latest_posts = get_all_posts()[:3]
    return render_template("home.html", posts=latest_posts, pages=get_all_pages_sorted())


@app.get("/blog/")
@cache.cached(timeout=60)
def render_blog_index():
    return render_template(
        "blog.html", title="Blog", posts=get_all_posts(), pages=get_all_pages_sorted()
    )


@app.get("/blog/<string:post_path>/")
@cache.memoize(timeout=3600)
def render_blog_post(post_path: str):
    post = get_single_post(post_path)

    if not post:
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


@app.post("/api/v1/post/")
@validate()
def create_post(body: PostCreateRequest):
    if request.headers.get("Authorization") != APP_SECRET:
        return "UNAUTHORIZED", 401
    
    try:
        url_slug = body.save()
    except HTTPError as e:
        return str(e), 400

    return f"{FQD}/blog/{url_slug}", 201
