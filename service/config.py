import os

SUPABASE_URL: str = os.environ["SUPABASE_URL"]
SUPBASE_KEY: str = os.environ["SUPABASE_KEY"]
APP_SECRET: str = os.environ["APP_SECRET"]
HIDE_NEW_POSTS: bool = bool(os.environ.get("HIDE_NEW_POSTS"))