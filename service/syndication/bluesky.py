from atproto import AsyncClient
from pydantic_settings import BaseSettings
from service.syndication.base import SyndicationService 

class BlueskyService(SyndicationService):
    def post(self, content: str, settings: BaseSettings):
        client = AsyncClient()
        client.login(settings.BSKY_HANDLE, settings.BSKY_PASSWORD)
        # TODO: The links are not being wrapped by Bluesky?
        client.send_post(text=content)