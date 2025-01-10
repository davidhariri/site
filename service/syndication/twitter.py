from pydantic_settings import BaseSettings
import tweepy
import asyncio
from service.syndication.base import SyndicationService

class TwitterService(SyndicationService):
    async def post(self, content: str, settings: BaseSettings):
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
        # Run the synchronous create_tweet in a thread pool
        await asyncio.to_thread(client.create_tweet, text=content)
