from pydantic import BaseModel, Field
from typing import Optional

class UserParticipant(BaseModel):
    id: Optional[str] = None
    name: str
    lastname: str
    username: str
    email: str
    accepted: bool = Field(default=False)
    banned: bool = Field(default=False)
    rolename: str = "Participant"


def parse_participant_from_mongo_dict(participant: dict) -> UserParticipant:
    print(participant)
    participant_obj = UserParticipant(
        id=str(participant["id"]),
        name=participant["name"],
        lastname=participant["lastname"],
        username=participant["username"],
        email=participant["email"],
        accepted=participant["accepted"],
        rolename=participant["rolename"]
    )

    return participant_obj
