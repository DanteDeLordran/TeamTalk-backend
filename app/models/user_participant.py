from pydantic import BaseModel


class UserParticipant(BaseModel):
    id: str | None
    name: str
    lastname: str
    username: str
    email: str
    accepted: bool = False
    rolename: str


def parse_participant_from_mongo_dict(participant: dict) -> UserParticipant:
    participant_obj = UserParticipant(
        id=participant["_id"],
        name=participant["name"],
        lastname=participant["lastname"],
        username=participant["username"],
        email=participant["email"],
        accepted=participant["accepted"],
        role=participant["rolename"]
    )

    return participant_obj
