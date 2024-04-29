from fastapi import APIRouter, Response, Header
from starlette.status import *
from ...models.message import Message, parse_message_to_mongo_dict, parse_message_from_mongo_dict
from ..services.default_returns import not_given_token, not_valid_token
from ...auth.token_service import authenticate
from ...db.db_context import db

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
