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
    S3_REGION: str = os.environ["S3_REGION"]
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    SENTRY_DSN: str | None = os.getenv("SENTRY_DSN")

settings = Settings()
