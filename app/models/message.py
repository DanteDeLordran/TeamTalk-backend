from pydantic import BaseModel
from datetime import datetime

from app.models.group import Group
from app.models.user_participant import UserParticipant


class Message(BaseModel):
    id: str | None
    user : UserParticipant
    message : str
    channel_id: str
    createdAt : datetime = datetime.now()
    
def parse_message_from_mongo_dict( message : dict ) -> Message:
    message_obj = Message(
        id= str(message["_id"]),
        user= message["user"],
        message= message["message"],
        channel_id=str(message["channel_id"]),
        createdAt=datetime.fromisoformat(message["createdAt"])
    )
    return message_obj