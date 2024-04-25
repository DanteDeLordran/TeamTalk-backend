from fastapi import APIRouter, Response, Header
from starlette.status import *
from ...models.user import parse_user_from_mongo_dict
from ...models.dto.user_register import UserRegister, build_user_from_register
from ...models.dto.user_login import UserLogin, build_login_dict
from ...models.dto.user_at_client import parse_user_from_mongo_dict
from ...db.db_context import db
from ...auth.token_service import get_user_token, authenticate
from ..services.validators import email_validator
import json

users_route = APIRouter()


@users_route.post('/register')
def register(userRegister: UserRegister):

    # Checking if any field is empy
    if check_if_register_empty(userRegister):
        return Response(status_code=HTTP_400_BAD_REQUEST,
                        media_type='application/json',
                        content=json.dumps({"message": "SOME_EMPY_FIELDS"}))

    if not email_validator(userRegister.email) or len(userRegister.email) < 5:
        return Response(status_code=HTTP_400_BAD_REQUEST,
                        media_type='application/json',
                        content=json.dumps({"message": "NOT_VALID_EMAIL"}))

    matching_user = db.users.find_one(
        {"$or": [{"email": userRegister.email}, {"username": userRegister.username}]})

    if matching_user != None:
        return Response(status_code=HTTP_400_BAD_REQUEST,
                        media_type='application/json',
                        content=json.dumps({"message": "USER_EXISTS"}))

    db.users.insert_one(build_user_from_register(userRegister))
    return Response(status_code=HTTP_204_NO_CONTENT)


@users_route.post('/login')
def login(userLogin: UserLogin):
    login_dict = build_login_dict(userLogin)
    matched_user = db.users.find_one(login_dict)

    if matched_user == None:
        return Response(status_code=HTTP_404_NOT_FOUND)

    user = parse_user_from_mongo_dict(matched_user)
    token = get_user_token(user)
    return token


@users_route.get('/authenticate')
def auth(token: str = Header(default=None)):
    if token == None:
        return Response(status_code=HTTP_400_BAD_REQUEST,
                        media_type='application/json',
                        content=json.dumps({"message": "NOT_GIVEN_TOKEN"}))

    user_result = authenticate(token)
    if user_result == None:
        return Response(status_code=HTTP_400_BAD_REQUEST,
                        media_type='application/json',
                        content=json.dumps({"message": "INVALID_TOKEN"}))

    return user_result


# Local Validators
def check_if_register_empty(userRegister: UserRegister) -> bool:
    return (len(userRegister.name) == 0
            or len(userRegister.lastname) == 0
            or len(userRegister.username) == 0
            or len(userRegister.password) == 0
            or len(userRegister.email) == 0)
