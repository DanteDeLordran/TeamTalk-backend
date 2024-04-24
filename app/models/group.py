from pydantic import BaseModel
from datetime import datetime
from .user_participant import UserParticipant


class Group(BaseModel):
    id: str | None
    name: str
    members: list[UserParticipant]
    creationDate: datetime
