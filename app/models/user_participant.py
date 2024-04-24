from pydantic import BaseModel
from .role import Role


class UserParticipant(BaseModel):
    id: str | None
    name: str
    lastname: str
    username: str
    email: str
    role: Role
