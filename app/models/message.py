from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Message(BaseModel):
    id: Optional[str] = None
    user_id : Optional[str] = None
    message : str
    channel_id: str
    createdAt : datetime = datetime.now()
    
def parse_message_from_mongo_dict( message : dict ) -> Message:
    message_obj = Message(
        id= str(message["_id"]),
        user_id=message["user_id"],
        message=message["message"],
        channel_id=str(message["channel_id"]),
        createdAt=message["createdAt"]
    )
    return message_obj


def parse_message_to_mongo_dict( message: Message ) -> dict:
    message_dict = message.model_dump()
    del message_dict["id"]

    return message_dict