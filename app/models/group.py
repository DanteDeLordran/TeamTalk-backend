from pydantic import BaseModel
from datetime import datetime
from .user_participant import UserParticipant, parse_participant_from_mongo_dict
from .role_definition import RoleDefinition, parse_role_from_mongo_dict
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
    creationDate: datetime = datetime.now()


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
