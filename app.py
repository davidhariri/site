import uuid
from urllib.parse import urljoin
import boto3
from botocore.exceptions import NoCredentialsError

from flask import abort, Flask, jsonify, render_template, request
from flask_caching import Cache
from rfeed import Item as RSSItem, Feed as RSSFeed  # type: ignore
import sentry_sdk
from slugify import slugify

from config import settings
from service.page import get_all_page_paths_and_pages, get_all_pages_sorted
from service.post import create_post, get_posts, get_posts_index

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

cache = Cache(config={"CACHE_TYPE": "SimpleCache"})
app = Flask(__name__)

cache.init_app(app)


@app.errorhandler(404)
def render_not_found(_):
    return render_template("404.html"), 404


@app.get("/")
@cache.cached(timeout=60)
def render_home():
    latest_posts = get_posts()[:3]
    return render_template(
        "home.html", posts=latest_posts, pages=get_all_pages_sorted()
    )


@app.get("/blog/")
@cache.cached(timeout=60, query_string=True)
def render_blog_index():
    tag = request.args.get("tagged")
    posts = get_posts()
    # TODO: We should just get this from the database more directly
    all_tags = sorted(set(tag for post in get_posts() for tag in (post.tags or [])), key=str.lower)
    
    if tag:
        posts = [post for post in posts if post.tags is not None and tag in post.tags]
    
    return render_template(
        "blog.html", title="Blog", posts=posts, tags=all_tags, tagged=tag, pages=get_all_pages_sorted()
    )


@app.get("/blog/<string:post_path>/")
@cache.memoize(timeout=3600)
def render_blog_post(post_path: str):
    try:
        post = get_posts_index()[post_path]
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
            link=f"{settings.FQD}/blog/{post.url_slug}",
            description=post.description or "",
            pubDate=post.date_published,
        )
        for post in get_posts()
    ]
    feed = RSSFeed( # TODO: Read this from a YAML config file
        title="David Hariri",
        link=f"{settings.FQD}/blog/",
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

# Micropub Logic

def verify_access_token() -> bool:
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return False
    token = auth_header.split(' ')[1]
    return token == settings.MICROPUB_SECRET

def upload_file_to_s3(file, bucket_name, file_key, acl="public-read"):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file_key,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except NoCredentialsError:
        abort(500, description="AWS credentials not available.")

@app.route('/micropub', methods=['GET', 'POST'])
def micropub():
    if request.method == 'GET':
        # Provide metadata about your Micropub endpoint
        response = {
            "actions": ["create", "update", "delete"],
            "types": ["h-entry"],
            "syndicate-to": [
                f"{settings.FQD}/blog/",
            ],
            "media-endpoint": f"{settings.FQD}/micropub/media/"
        }
        return jsonify(response)
    elif request.method == 'POST':
        if not verify_access_token():
            abort(401, description="Invalid or missing access token.")
    
        data = request.get_json()
        if not data:
            abort(400, description="Invalid JSON payload.")
        
        h = data.get('type', ['entry'])[0]  # default to 'entry'
        if h != 'h-entry':
            abort(400, description="Unsupported type.")

        properties = data.get('properties', {})
        content_list = properties.get('content', [''])

        if not isinstance(content_list, list) or not content_list or not isinstance(content_list[0], str):
            abort(400, description="Invalid content format.")
        
        content = content_list[0].strip()
        
        if not content:
            abort(400, description="Missing content.")

        title = properties.get('name', [None])[0]
        categories = properties.get('category', [])  # tags

        url_slug = slugify(title) if title else str(uuid.uuid4())

        post = create_post(
            title=title,
            content=content,
            url_slug=url_slug,
            tags=set(categories) if categories else None,
            description=properties.get('summary', [None])[0]
        )

        post_url = urljoin(settings.FQD, f"/blog/{post.url_slug}/")

        response = jsonify({"url": post_url})
        response.status_code = 201
        response.headers['Location'] = post_url
        return response

@app.route('/micropub/media/', methods=['POST'])
def micropub_media():    
    if not verify_access_token():
        abort(401, description="Invalid or missing access token.")
    
    if 'file' not in request.files:
        abort(400, description="No file part in the request.")
    
    file = request.files['file']
    if file.filename == '':
        abort(400, description="No selected file.")
    
    # Check the file size using the Content-Length header
    content_length = request.headers.get('Content-Length', type=int)
    if content_length is not None and content_length > 10 * 1024 * 1024:  # 10 MB
        abort(400, description="File is too large.")
    
    allowed_extensions = {'gif', 'jpg', 'jpeg', 'png', 'webp', 'mp4'}
    file_ext = file.filename.rsplit('.', 1)[-1].lower()
    if file_ext not in allowed_extensions:
        abort(400, description="Unsupported file type.")
    
    # Generate a unique filename
    unique_filename = f"{uuid.uuid4()}.{file_ext}"
    
    # Upload the file to S3
    upload_file_to_s3(file, settings.S3_BUCKET_NAME, unique_filename)
    
    file_url = f"https://{settings.S3_BUCKET_NAME}.s3.amazonaws.com/{unique_filename}"
    response = jsonify({"url": file_url})
    response.status_code = 201
    response.headers['Location'] = file_url
    return response
