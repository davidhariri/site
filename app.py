import uuid
from urllib.parse import urljoin
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

from flask import abort, Flask, jsonify, render_template, request
from rfeed import Item as RSSItem, Feed as RSSFeed  # type: ignore
import sentry_sdk
from slugify import slugify
import tweepy
from atproto import Client as AtProtoSyncClient

from config import settings
from service.page import get_all_page_paths_and_pages, get_all_pages_sorted
from service.post import create_post, get_all_tags, get_posts, get_posts_index

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app = Flask(__name__)
app.jinja_env.auto_reload = settings.DEBUG


@app.context_processor
def inject_globals():
    """Inject global variables into the Jinja context for all templates`"""
    return {
        "og_title": settings.OG_TITLE,
        "og_description": settings.OG_DESCRIPTION,
        "og_url": settings.OG_URL,
    }


@app.errorhandler(404)
def render_not_found(_):
    """Display the custom 404 page"""
    return render_template("404.html"), 404


@app.get("/")
def render_home():
    """Display the main home page with the latest posts"""
    latest_posts = get_posts()[:3]
    return render_template(
        "home.html", posts=latest_posts, pages=get_all_pages_sorted()
    )


@app.get("/blog/")
def render_blog_index():
    """Display the blog index page with all posts"""
    # TODO: This should be paginated
    tag = request.args.get("tagged")
    posts = get_posts()
    all_tags = get_all_tags()

    if tag:
        posts = [post for post in posts if post.tags is not None and tag in post.tags]

    return render_template(
        "blog.html",
        title="Blog",
        posts=posts,
        tags=all_tags,
        tagged=tag,
        pages=get_all_pages_sorted(),
    )


@app.get("/blog/<string:post_path>/")
def render_blog_post(post_path: str):
    """Display a single blog post"""
    try:
        post = get_posts_index()[post_path]
    except KeyError:
        abort(404)

    return render_template("blog_post.html", post=post, pages=get_all_pages_sorted())


@app.get("/feed/")
@app.get("/rss/")
def read_feed():
    """Generate an RSS feed for all blog posts"""
    items = [
        RSSItem(
            title=post.title,
            link=f"{settings.FQD}/blog/{post.url_slug}",
            description=post.description or "",
            pubDate=post.date_published,
        )
        for post in get_posts()
    ]
    feed = RSSFeed(  # TODO: Read this from a YAML config file
        title="David Hariri",
        link=f"{settings.FQD}/blog/",
        description="The blog of David Hariri. Programming, design, and more.",
        language="en-US",
        lastBuildDate=items[0].pubDate,
        items=items,
    )
    return feed.rss()


@app.get("/<string:page_path>/")
def render_page(page_path: str):
    """Display a single page"""
    try:
        page = get_all_page_paths_and_pages()[page_path]
    except KeyError:
        abort(404)

    return render_template("page.html", page=page, pages=get_all_pages_sorted())


# Micropub Logic


def verify_access_token() -> bool:
    """
    Verify the access token in the Authorization header.
    """
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return False
    token = auth_header.split(" ")[1]
    return token == settings.MICROPUB_SECRET


def upload_file_to_s3(file, bucket_name, file_key):
    """
    Upload a file to an S3 bucket.
    """
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
    )
    try:
        s3.upload_fileobj(
            file, bucket_name, file_key, ExtraArgs={"ContentType": file.content_type}
        )
    except NoCredentialsError:
        abort(500, description="AWS credentials not available.")
    except ClientError as e:
        abort(500, description=f"Client error: {e}")


def post_tweet(post_content: str):
    """
    Post a tweet to Twitter.
    """
    client = tweepy.Client(
        bearer_token=settings.TWITTER_API_BEARER_TOKEN,
        consumer_key=settings.TWITTER_API_CONSUMER_KEY,
        consumer_secret=settings.TWITTER_API_CONSUMER_SECRET,
        access_token=settings.TWITTER_API_ACCESS_TOKEN,
        access_token_secret=settings.TWITTER_API_ACCESS_TOKEN_SECRET,
    )
    client.create_tweet(text=post_content)


def post_bsky(post_content: str):
    """
    Post a blog post to bluesky
    """
    client = AtProtoSyncClient()
    client.login(settings.BSKY_HANDLE, settings.BSKY_PASSWORD)
    client.send_post(text=post_content)


@app.route("/micropub", methods=["GET", "POST"])
def micropub():
    """
    Micropub endpoint for creating, updating, and deleting posts.
    """
    if request.method == "GET":
        # Provide metadata about your Micropub endpoint
        response = {
            "actions": ["create", "update", "delete"],
            "types": ["h-entry"],
            "syndicate-to": [
                f"{settings.FQD}/blog/",
            ],
            "media-endpoint": f"{settings.FQD}/micropub/media/",
        }
        return jsonify(response)
    elif request.method == "POST":
        if not verify_access_token():
            abort(401, description="Invalid or missing access token.")

        data = request.get_json()
        if not data:
            abort(400, description="Invalid JSON payload.")

        h = data.get("type", ["entry"])[0]  # default to 'entry'
        if h != "h-entry":
            abort(400, description="Unsupported type.")

        properties = data.get("properties", {})
        content_list = properties.get("content", [""])

        if (
            not isinstance(content_list, list)
            or not content_list
            or not isinstance(content_list[0], str)
        ):
            abort(400, description="Invalid content format.")

        content = content_list[0].strip()

        if not content:
            abort(400, description="Missing content.")

        title = properties.get("name", [None])[0]
        categories = properties.get("category", [])  # tags

        url_slug = slugify(title) if title else str(uuid.uuid4())

        result = create_post(
            title=title,
            content=content,
            url_slug=url_slug,
            tags=set(categories) if categories else None,
            description=properties.get("summary", [None])[0],
        )
        post = result.post
        updated_existing = result.updated_existing

        post_url = urljoin(settings.FQD, f"/blog/{post.url_slug}/")
        post_social_content = f"{post.title}\n\n{post.description}\n\n🔗 {post_url}"

        # Post to Twitter if configured in the environment
        if settings.TWITTER_API_BEARER_TOKEN and not updated_existing:
            # NOTE: You need more than just a bearer token to use the Twitter API
            #   to post to your own account, this is just a simple way to see if any ENV
            #   variables are set for the Twitter API.
            try:
                post_tweet(post_social_content)
            except Exception as e:
                sentry_sdk.capture_exception(e)

        # Post to bluesky if configured in the environment
        if settings.BSKY_HANDLE and settings.BSKY_PASSWORD and not updated_existing:
            try:
                post_bsky(post_social_content)
            except Exception as e:
                sentry_sdk.capture_exception(e)

        response = jsonify({"url": post_url})
        response.status_code = 201
        response.headers["Location"] = post_url
        return response


@app.route("/micropub/media/", methods=["POST"])
def micropub_media():
    """MicroPub media endpoint for uploading files."""
    if not verify_access_token():
        abort(401, description="Invalid or missing access token.")

    if "file" not in request.files:
        abort(400, description="No file part in the request.")

    file = request.files["file"]
    if file.filename == "":
        abort(400, description="No selected file.")

    # Check the file size using the Content-Length header
    content_length = request.headers.get("Content-Length", type=int)
    if content_length is not None and content_length > 10 * 1024 * 1024:  # 10 MB
        abort(400, description="File is too large.")

    allowed_extensions = {"gif", "jpg", "jpeg", "png", "webp", "mp4"}
    file_ext = file.filename.rsplit(".", 1)[-1].lower()
    if file_ext not in allowed_extensions:
        abort(400, description="Unsupported file type.")

    # Generate a unique filename
    unique_filename = f"{uuid.uuid4()}.{file_ext}"

    # Upload the file to S3
    upload_file_to_s3(file, settings.S3_BUCKET_NAME, unique_filename)

    file_url = f"https://{settings.S3_BUCKET_NAME}.s3.amazonaws.com/{unique_filename}"
    response = jsonify({"url": file_url})
    response.status_code = 201
    response.headers["Location"] = file_url
    return response
