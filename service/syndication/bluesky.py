from atproto import AsyncClient
from pydantic_settings import BaseSettings
from service.syndication.base import SyndicationService 

class BlueskyService(SyndicationService):
    async def post(self, content: str, settings: BaseSettings):
        client = AsyncClient()
        await client.login(settings.BSKY_HANDLE, settings.BSKY_PASSWORD)
        # TODO: The links are not being wrapped by Bluesky?
        await client.send_post(text=content)