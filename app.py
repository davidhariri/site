import os
from flask import abort, Flask, render_template
from rfeed import Item as RSSItem, Feed as RSSFeed


from service.blogpost import BlogPost
from service.page import Page

app = Flask(__name__)

all_content: dict[str, dict[str, Page | BlogPost]] = {}

for dir in ["pages", "blog"]:
    all_content[dir] = {}

    for file_name in os.listdir(dir):
        with open(f"{dir}/{file_name}", "r") as post_file:
            if dir == "pages":
                content = Page.from_file(file_name, post_file)
            else:
                content = BlogPost.from_file(file_name, post_file)

            all_content[dir][content.path] = content


@app.errorhandler(404)
def page_not_found(_):
    return render_template("404.html"), 404


@app.get("/")
def render_home():
    latest_posts = sorted(
        all_content["blog"].values(), key=lambda post: post.date, reverse=True
    )[:3]
    pages = all_content["pages"].values()
    return render_template("home.html", posts=latest_posts, pages=pages)


@app.get("/blog/")
def render_blog_index():
    return render_template(
        "blog.html", title="Blog", posts=all_content["blog"].values()
    )


@app.get("/feed/")
@app.get("/rss/")
def render_feed():
    fqd = "https://dhariri.com"
    items = [
        RSSItem(
            title=post.title,
            link=f"{fqd}/blog/{post.path}",
            description=post.html_content,
            pubDate=post.date,
        )
        for post in all_content["blog"].values()
    ]
    feed = RSSFeed(
        title="David Hariri",
        link=f"{fqd}/blog/",
        description="The blog of David Hariri. Programming, design, and more.",
        language="en-US",
        lastBuildDate=items[0].pubDate,
        items=items,
    )
    print(feed.rss())
    return feed.rss()


@app.get("/<page_path>/")
def render_page(page_path: str):
    try:
        page = all_content["pages"][page_path]
    except KeyError:
        abort(404)

    return render_template("page.html", page=page)


@app.get("/blog/<post_path>/")
def render_blog_post(post_path: str):
    try:
        post = all_content["blog"][post_path]
    except KeyError:
        abort(404)

    return render_template("page.html", page=post)
