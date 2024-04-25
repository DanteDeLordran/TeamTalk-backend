from pydantic import BaseModel
from datetime import datetime
from .user_participant import UserParticipant
from .role_definition import RoleDefinition
from .admin import Admin
from .normal_participant import NormalParticipant

class Group(BaseModel):
    id: str | None
    name: str
    members: list[UserParticipant]
    roles: list[RoleDefinition] = [
        Admin(),
        NormalParticipant()
    ]
    creationDate: datetime
