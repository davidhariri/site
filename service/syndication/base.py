from abc import ABC, abstractmethod
from pydantic_settings import BaseSettings

class SyndicationService(ABC):
    @abstractmethod
    def post(self, content: str, settings: BaseSettings):
        pass
