from pydantic import BaseModel
from typing import Optional

class Channel(BaseModel):
    id: Optional[str] = None
    group_id: str
    channel_name: str

def parse_channel_from_mongo_dict(channel: dict) -> Channel:
    channel_obj = Channel(
        id=str(channel["_id"]),
        group_id=channel["group_id"],
        channel_name=channel["channel_name"]
    )

    return channel_obj

def parse_channel_to_mongo_dict(channel: Channel) -> dict:
    channel_dict = channel.model_dump()
    del channel_dict["id"]

    return channel_dict