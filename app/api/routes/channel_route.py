from fastapi import APIRouter, Response, Header
from starlette.status import *
from ...db.db_context import db
from ...auth.token_service import authenticate
from ...models.channel import Channel, ChannelRequest, parse_channel_to_mongo_dict, parse_channel_from_mongo_dict
import json
from ..services.default_returns import not_given_token, not_valid_token
from bson import ObjectId

channel_route = APIRouter()

@channel_route.post('/create')
def create_channer(request: ChannelRequest, token: str = Header(default=None)):
    if token == None:
        return not_given_token()

    user = authenticate(token)
    if user == None:
        return not_valid_token()
    
    matching_channel_on_group = db.channels.find_one({"group_id": request.group_id, "channel_name": request.channel_name})
    if matching_channel_on_group != None:
        return Response(status_code=HTTP_400_BAD_REQUEST,
                        media_type='application/json',
                        content=json.dumps({"message": "EXISTING_CHANNEL"}))

    channel = Channel(
        group_id= request.group_id,
        channel_name=request.channel_name
    )

    channel_dict = parse_channel_to_mongo_dict(channel) 
    channel_id = str(db.channels.insert_one(channel_dict).inserted_id)

    channel_result = db.channels.find_one({"_id": ObjectId(channel_id)})
    channel_obj = parse_channel_from_mongo_dict(channel_result)

    return Response(
        status_code=HTTP_201_CREATED
    )

@channel_route.get('/All/{group_id}')
def get_all_channel_withing_group(group_id: str, token: str = Header(default=None)):
    if token == None:
        return not_given_token()
    
    user = authenticate(token)

    if user == None:
        return not_valid_token()
    
    channels = list(db.channels.find({"group_id": group_id}))

    channels_objs = [parse_channel_from_mongo_dict(ch) for ch in channels]
    channel_dicts = [ch.model_dump() for ch in  channels_objs]

    return channel_dicts
