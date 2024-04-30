from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .user_participant import UserParticipant, parse_participant_from_mongo_dict
from .role_definition import RoleDefinition, parse_role_from_mongo_dict
from .admin import Admin
from .normal_participant import NormalParticipant


class Group(BaseModel):
    id: Optional[str] = None
    name: str
    members: list[UserParticipant] = Field(default=[])
    roles: list[RoleDefinition] = Field(default=[
        Admin(),
        NormalParticipant()
    ])
    creationDate: datetime = Field(default=datetime.now())

class GroupRequest(BaseModel):
    name : str = Field(min_length=2)

def parse_group_from_mongo_dict(group: dict) -> Group:
    group_obj = Group(
        id=str(group["_id"]),
        name=group["name"],
        members=[parse_participant_from_mongo_dict(
            user) for user in group["members"]],
        roles=[parse_role_from_mongo_dict(role) for role in group["roles"]],
        creationDate=datetime.fromisoformat(group["creationDate"])
    )

    return group_obj

def parse_group_to_mongo_dict(group: Group) -> dict:
    group_dict = group.model_dump()
    del group_dict["id"]

    group_dict["creationDate"] = datetime.isoformat(group.creationDate)
    return group_dict