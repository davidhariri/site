from abc import ABC, abstractmethod
from pydantic_settings import BaseSettings

class SyndicationService(ABC):
    @abstractmethod
    async def post(self, content: str, settings: BaseSettings):
        pass
