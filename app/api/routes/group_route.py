from fastapi import APIRouter, Response, Header
from starlette.status import *
from bson import ObjectId
import json
from ...db.db_context import db
from ...auth.token_service import authenticate
from ...models.group import Group, parse_group_from_mongo_dict, parse_group_to_mongo_dict
from ...models.user_participant import UserParticipant
from ..services.default_returns import not_given_token, not_valid_token

group_route = APIRouter()

@group_route.post('/create')
def create_group(group: Group, token: str = Header(default=None)):
    if token == None:
        return not_given_token()
    
    user = authenticate(token)

    if user == None:
        return not_valid_token()
    
    if len(group.name) == 0:
        return Response(status_code=HTTP_400_BAD_REQUEST,
                        media_type='appliation/json',
                        content=json.dumps({"message": "NOT_GIVEN_NAME"}))
    
    # make user an admin participant
    admin = UserParticipant(
        id=user.id,
        name=user.name,
        lastname=user.lastname,
        username=user.username,
        email=user.email,
        accepted=True,
        banned=False,
        rolename="Admin"
    )

    group.members.append(admin)

    # Parse to mongo dict
    group_to_mongo = parse_group_to_mongo_dict(group)

    group_id = str(db.groups.insert_one(group_to_mongo).inserted_id)

    group_result = parse_group_from_mongo_dict(db.groups.find_one({"_id": ObjectId(group_id)}))

    return group_result

@group_route.get('/All')
def get_user_groups(token: str = Header(default=None)):
    if token == None:
        return not_given_token()
    
    user = authenticate(token)
    if user == None:
        return not_valid_token()
    
    groups = list(db.groups.find({"members": {"$elemMatch": {"id": user.id}}}))
    print(groups)
    group_objs = [parse_group_from_mongo_dict(group) for group in groups]
    return [parse_group_to_mongo_dict(group) for group in group_objs]