from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import os

load_dotenv()


class Settings(BaseSettings):
    MONGODB_URI: str = os.environ["MONGODB_URI"]
    DATABASE_NAME: str = os.environ["DATABASE_NAME"]
    MICROPUB_SECRET: str = os.environ["MICROPUB_SECRET"]
    FQD: str = os.environ["FQD"]
    S3_ACCESS_KEY: str = os.environ["S3_ACCESS_KEY"]
    S3_SECRET_KEY: str = os.environ["S3_SECRET_KEY"]
    S3_BUCKET_NAME: str = os.environ["S3_BUCKET_NAME"]
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    SENTRY_DSN: str | None = os.getenv("SENTRY_DSN")
    TWITTER_API_CONSUMER_KEY: str | None = os.getenv("TWITTER_API_CONSUMER_KEY")
    TWITTER_API_CONSUMER_SECRET: str | None = os.getenv("TWITTER_API_CONSUMER_SECRET")
    TWITTER_API_ACCESS_TOKEN: str | None = os.getenv("TWITTER_API_ACCESS_TOKEN")
    TWITTER_API_ACCESS_TOKEN_SECRET: str | None = os.getenv(
        "TWITTER_API_ACCESS_TOKEN_SECRET"
    )
    TWITTER_API_BEARER_TOKEN: str | None = os.getenv("TWITTER_API_BEARER_TOKEN")
    DEBUG: bool = os.getenv("FLASK_DEBUG") == "1"
    OG_TITLE: str = "David Hariri"
    OG_URL: str = "https://dhariri.com"
    OG_DESCRIPTION: str = "David's place on the web"
    BSKY_HANDLE: str | None = os.getenv("BSKY_HANDLE")
    BSKY_PASSWORD: str | None = os.getenv("BSKY_PASSWORD")


settings = Settings()
