import logging
import uuid
from urllib.parse import urljoin

from quart import abort, Quart, jsonify, render_template, request
from botocore.exceptions import NoCredentialsError, ClientError

from rfeed import Item as RSSItem, Feed as RSSFeed  # type: ignore
import sentry_sdk
from slugify import slugify
from service.syndication import TwitterService, BlueskyService

from config import settings
from service.page import get_all_page_paths_and_pages, get_all_pages_sorted
from service.post import create_post, get_all_tags, get_posts, get_posts_index
from service.micropub import verify_access_token, upload_file_to_s3

logger = logging.getLogger(__name__)

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app = Quart(__name__)
app.jinja_env.auto_reload = settings.DEBUG


@app.context_processor
async def inject_globals():
    """Inject global variables into the Jinja context for all templates`"""
    return {
        "og_title": settings.OG_TITLE,
        "og_description": settings.OG_DESCRIPTION,
        "og_url": settings.OG_URL,
    }


@app.errorhandler(404)
async def render_not_found(_):
    """Display the custom 404 page"""
    return await render_template("404.html"), 404


@app.get("/")
async def render_home():
    """Display the main home page with the latest posts"""
    return await render_template(
        "home.html",
        posts=await get_posts(),
        pages=await get_all_pages_sorted(),
    )


@app.get("/blog/")
async def render_blog_index():
    """Display the blog index page with all posts"""
    tag = request.args.get("tagged")
    posts = await get_posts()
    all_tags = await get_all_tags()

    if tag:
        posts = [post for post in posts if post.tags is not None and tag in post.tags]

    return await render_template(
        "blog.html",
        title="Blog",
        posts=posts,
        tags=all_tags,
        tagged=tag,
        pages=await get_all_pages_sorted(),
    )


@app.get("/blog/<string:post_path>/")
async def render_blog_post(post_path: str):
    """Display a single blog post"""
    try:
        posts_index = await get_posts_index()
        post = posts_index[post_path]
    except KeyError:
        abort(404)

    return await render_template("blog_post.html", post=post, pages=await get_all_pages_sorted())


@app.get("/feed/")
async def read_feed():
    """Generate an RSS feed for all blog posts"""
    posts = await get_posts()
    items = [
        RSSItem(
            title=post.title,
            link=f"{settings.FQD}/blog/{post.url_slug}",
            description=post.description or "",
            pubDate=post.date_published,
        )
        for post in posts
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


@app.get("/rss/")
async def read_rss_feed():
    """Alias for /feed/ endpoint"""
    return await read_feed()


@app.get("/<string:page_path>/")
async def render_page(page_path: str):
    """Display a single page"""
    try:
        pages = await get_all_page_paths_and_pages()
        page = pages[page_path]
    except KeyError:
        abort(404)

    return await render_template("page.html", page=page, pages=await get_all_pages_sorted())


@app.route("/micropub", methods=["GET", "POST"])
async def micropub_api():
    """
    Micropub endpoint for creating, updating, and deleting posts.
    """
    if request.method == "GET":
        # Provide metadata about the Micropub endpoint
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
        if not verify_access_token(request, settings):
            abort(401, description="Invalid or missing access token.")

        data = await request.get_json()
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

        result = await create_post(
            title=title,
            content=content,
            url_slug=url_slug,
            tags=set(categories) if categories else None,
            description=properties.get("summary", [None])[0],
        )
        post = result.post

        post_url = urljoin(settings.FQD, f"/blog/{post.url_slug}/")
        post_social_content = f"{post.title}\n\n{post.description}\n\n🔗 {post_url}"

        for service in [TwitterService(), BlueskyService()]:
            try:
                await service.post(content=post_social_content, settings=settings)
            except Exception as e:
                logger.error(f"Error posting to {service.__class__.__name__}: {e}")
                continue

        response = jsonify({"url": post_url})
        response.status_code = 201
        response.headers["Location"] = post_url
        return response


@app.route("/micropub/media/", methods=["POST"])
async def micropub_media():
    """MicroPub media endpoint for uploading files."""
    if not await verify_access_token():
        abort(401, description="Invalid or missing access token.")

    files = await request.files
    if "file" not in files:
        abort(400, description="No file part in the request.")

    file = files["file"]
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
    try:
        await upload_file_to_s3(file, settings.S3_BUCKET_NAME, unique_filename)
    except NoCredentialsError:
        abort(500, description="AWS credentials not available.")
    except ClientError as e:
        abort(500, description=f"Client error: {e}")

    file_url = f"https://{settings.S3_BUCKET_NAME}.s3.amazonaws.com/{unique_filename}"
    response = jsonify({"url": file_url})
    response.status_code = 201
    response.headers["Location"] = file_url
    return response


@app.after_request
async def add_cache_headers(response):
    # Add cache headers for static files
    if response.mimetype in ['text/css', 'text/javascript', 'image/svg+xml', 'image/png', 'image/jpeg']:
        response.cache_control.max_age = 31536000  # 1 year
        response.cache_control.public = True
    return response
