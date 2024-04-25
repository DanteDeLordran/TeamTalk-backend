from fastapi import APIRouter, Response, Header
from starlette.status import *
from ...models.user import parse_user_from_mongo_dict
from ...models.dto.user_register import UserRegister, build_user_from_register
from ...models.dto.user_login import UserLogin, build_login_dict
from ...models.dto.user_at_client import parse_user_from_mongo_dict
from ...db.db_context import db
from ...auth.token_service import get_user_token, authenticate

users_route = APIRouter()


@users_route.post('/register')
def register(userRegister: UserRegister):
    matching_user = db.users.find_one(
        {"$or": [{"email": userRegister.email}, {"username": userRegister.username}]})

    if matching_user != None:
        return Response(status_code=HTTP_400_BAD_REQUEST, content="USER_EXISTS")

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
        return Response(status_code=HTTP_400_BAD_REQUEST, content="NOT_GIVEN_TOKEN")
    user_result = authenticate(token)
    if user_result == None:
        return Response(status_code=HTTP_400_BAD_REQUEST, content="INVALID_TOKEN")
    return user_result
