
from pydantic import BaseModel

from app.models.group import Group
from app.models.user import User


class Message(BaseModel):
    id: str | None
    user : User
    message : str
    group : Group
    createdAt : str
    
def parse_message_from_mongo_dict( message : dict ) -> Message:
    message_obj = Message(
        id= str(message["_id"]),
        user= message["user"],
        message= message["message"],
        group=message["group"],
        createdAt=message["createdAt"]
    )
    return message_obj