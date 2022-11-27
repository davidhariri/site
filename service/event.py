from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class Event(BaseModel):
    """
    An event, stored in the database.
    """
    id: int
    date_created: datetime
    user_id: UUID
    date_published: datetime
    ip_address: str
    type: str
    title: str
    referrer: str
    device: str
    os: str