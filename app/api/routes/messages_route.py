from fastapi import APIRouter, Response, Header
from starlette.status import *
from ...models.message import Message, parse_message_to_mongo_dict, parse_message_from_mongo_dict
from ...models.channel import parse_channel_from_mongo_dict
from ...models.group import Group, parse_group_from_mongo_dict
from ...models.role_definition import RoleDefinition
from ...models.user_participant import UserParticipant, parse_participant_from_mongo_dict
from ..services.default_returns import not_given_token, not_valid_token
from ...auth.token_service import authenticate
from ...db.db_context import db
from bson import ObjectId
import json

messages_route = APIRouter()


@messages_route.post('/send')
def send_message(message: Message, token: str = Header(default=None)):
    if token == None:
        return not_given_token()

    user = authenticate(token)

    if user is None:
        return not_valid_token()

    user_id = user.id

    message.user_id = user_id
    message_dict = parse_message_to_mongo_dict(message)

    id = db.messages.insert_one(message_dict).inserted_id
    message.id = str(id)

    return message


@messages_route.get('/get/{channel_id}')
def get_messages_from_group(channel_id: str, token: str = Header(default=None)):
    if token is None:
        return not_given_token()

    user = authenticate(token)

    if user is None:
        return not_valid_token()
    
    message_dict_list = list(db.messages.find({"channel_id": channel_id}))

    messages = [parse_message_from_mongo_dict(msg) for msg in message_dict_list]

    return messages


@messages_route.delete('/delete/{message_id}')
def delete_message(message_id: str, token: str = Header(default=None)):
    if token is None:
        return not_given_token()
    
    user = authenticate(token)

    if user is None:
        return not_valid_token()
    
    message_dict = db.messages.find_one({"_id": ObjectId(message_id)})

    if message_dict is None:
        return Response(status_code=HTTP_404_NOT_FOUND)

    message = parse_message_from_mongo_dict(message_dict)

    channel_dict = db.channels.find_one({"_id": ObjectId(message.channel_id)})
    channel = parse_channel_from_mongo_dict(channel_dict)

    group_dict = db.groups.find_one({"_id": ObjectId(channel.group_id)})
    group = parse_group_from_mongo_dict(group_dict)

    participant = extract_participant(group, user.id)

    if participant is None:
        return Response(status_code=HTTP_401_UNAUTHORIZED,
                        media_type="application/json",
                        content=json.dumps({"message": "NOT_PARTICIPANT"}))
    
    role = extract_role(group, participant)

    if message.user_id == participant.id:
        if role.can_delete_messages:
            db.messages.delete_one({"_id": ObjectId(message.id)})
            return Response(status_code=HTTP_200_OK)
        return Response(status_code=HTTP_403_FORBIDDEN)
    
    if not role.can_delete_others_messages:
        return Response(status_code=HTTP_403_FORBIDDEN)

    db.messages.delete_one({"_id": ObjectId(message.id)})
    return Response(status_code=HTTP_200_OK)
    



def extract_participant(group: Group, id: str) -> UserParticipant | None:
    for participant in group.members:
        if participant.id == id:
            return participant
        
    return None


def extract_role(group: Group, participant: UserParticipant) -> RoleDefinition:
    for role in group.roles:
        if role.rolename == participant.rolename:
            return role