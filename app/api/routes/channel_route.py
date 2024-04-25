from fastapi import APIRouter, Response, Header
from starlette.status import *
from ...db.db_context import db
from ...auth.token_service import authenticate
from ...models.channel import Channel, parse_channel_to_mongo_dict, parse_channel_from_mongo_dict
import json
from bson import ObjectId

channel_route = APIRouter()

@channel_route.post('/create')
def create_channer(channel: Channel, token: str = Header(default=None)):
    if token == None:
        return Response(status_code=HTTP_400_BAD_REQUEST,
                        media_type='application/json',
                        content=json.dumps({"message": "NOT_GIVEN_TOKEN"}))

    user = authenticate(token)
    if user == None:
        return Response(status_code=HTTP_400_BAD_REQUEST,
                        media_type='application/json',
                        content=json.dumps({"message": "NOT_VALID_TOKEB"}))
    
    matching_channel_on_group = db.channels.find_one({"group_id": channel.group_id, "channel_name": channel.channel_name})
    if matching_channel_on_group != None:
        return Response(status_code=HTTP_400_BAD_REQUEST,
                        media_type='application/json',
                        content=json.dumps({"message": "EXISTING_CHANNEL"}))

    channel_dict = parse_channel_to_mongo_dict(channel) 
    channel_id = str(db.channels.insert_one(channel_dict).inserted_id)

    channel_result = db.channels.find_one({"_id": ObjectId(channel_id)})
    channel_obj = parse_channel_from_mongo_dict(channel_result)

    return channel_obj
