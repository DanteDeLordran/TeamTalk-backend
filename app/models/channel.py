from pydantic import BaseModel

class Channel(BaseModel):
    id: str | None
    group_id: str
    channel_name: str

def parse_channel_from_mongo_dict(channel: dict) -> Channel:
    channel_obj = Channel(
        id=str(channel["_id"]),
        group_id=channel["group_id"],
        channel_name=channel["channel_name"]
    )

    return channel_obj