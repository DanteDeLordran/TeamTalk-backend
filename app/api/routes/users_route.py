from fastapi import APIRouter, Response, Header
from starlette.status import *
from ...models.user import User, UserRequest, parse_user_from_mongo_dict
from ...models.dto.user_register import UserRegister, build_user_from_register
from ...models.dto.user_login import UserLogin, build_login_dict
from ...models.dto.user_at_client import parse_user_from_mongo_dict
from ...db.db_context import db
from ...auth.token_service import get_user_token, authenticate
from ..services.validators import email_validator, password_validator
import json
from ..services.default_returns import not_valid_token, not_given_token
from bson import ObjectId

users_route = APIRouter()


@users_route.post('/register')
def register(userRegister: UserRegister):

    # Checking if any field is empy
    if check_if_register_empty(userRegister):
        return Response(status_code=HTTP_400_BAD_REQUEST,
                        media_type='application/json',
                        content=json.dumps({"message": "SOME_EMPY_FIELDS"}))

    # Checking if email is valid
    if not email_validator(userRegister.email) or len(userRegister.email) < 5:
        return Response(status_code=HTTP_400_BAD_REQUEST,
                        media_type='application/json',
                        content=json.dumps({"message": "NOT_VALID_EMAIL"}))

    if not password_validator(userRegister.password):
        return Response(status_code=HTTP_400_BAD_REQUEST,
                        media_type='application/json',
                        content=json.dumps({"message": "NOT_VALID_PASSWORD"}))

    matching_user = db.users.find_one(
        {"$or": [{"email": userRegister.email}, {"username": userRegister.username}]})

    if matching_user != None:
        return Response(status_code=HTTP_400_BAD_REQUEST,
                        media_type='application/json',
                        content=json.dumps({"message": "USER_EXISTS"}))

    db.users.insert_one(build_user_from_register(userRegister))
    return Response(status_code=HTTP_201_CREATED)


@users_route.post('/login')
def login(userLogin: UserLogin):
    login_dict = build_login_dict(userLogin)

    if not email_validator(userLogin.email):
        return Response(status_code=HTTP_400_BAD_REQUEST,
                        media_type='application/json',
                        content=json.dumps({"message": "NOT_VALID_EMAIL"}))

    if not password_validator(userLogin.password):
        return Response(status_code=HTTP_400_BAD_REQUEST,
                        media_type='application/json',
                        content=json.dumps({"message": "NOT_VALID_PASSWORD"}))

    matched_user = db.users.find_one(login_dict)

    if matched_user == None:
        return Response(status_code=HTTP_404_NOT_FOUND)

    user = parse_user_from_mongo_dict(matched_user)
    token = get_user_token(user)
    return token


@users_route.get('/authenticate')
def auth(token: str = Header(default=None)):
    if token == None:
        return not_given_token()

    user_result = authenticate(token)
    if user_result == None:
        return not_valid_token()

    return user_result


@users_route.put('/edit')
async def edit_user(request: UserRequest, token: str = Header(default=None)):
    if token == None:
        return not_given_token()

    user_result = authenticate(token)

    if user_result == None:
        return not_valid_token()

    _id = ObjectId(user_result.id)

    matching_user_username = db.users.find_one(
        {
            '$and': [
                {'_id': {'$ne': _id}}, 
                {'username': request.username}
            ]
        }
    )

    print('matching username: ', matching_user_username)

    if matching_user_username != None:
        return Response(status_code=HTTP_400_BAD_REQUEST,
                        media_type='application/json',
                        content=json.dumps({"message": "TAKEN_USERNAME"}))

    matching_user_email = db.users.find_one(
        {
            '$and': 
            [
                {'_id':  {'$ne': _id}},
                {'email': request.email}
            ]
        }
    )

    print('email matching: ', matching_user_email)

    if matching_user_email != None:
        return Response(status_code=HTTP_400_BAD_REQUEST,
                        media_type='application/json',
                        content=json.dumps({"message": "TAKEN_EMAIL"}))

    if not email_validator(request.email):
        return Response(status_code=HTTP_400_BAD_REQUEST,
                        media_type='application/json',
                        content=json.dumps({'message': 'NOT_VALID_EMAIL'}))

    db.users.update_one(
        {
            '_id': _id
        },
        {
            '$set': {
                "email": request.email,
                "name": request.name,
                "lastname": request.lastname,
                "username": request.username
            }
        }
    )

    return Response(status_code=200)

# Local Validators


def check_if_register_empty(userRegister: UserRegister) -> bool:
    return (len(userRegister.name) == 0
            or len(userRegister.lastname) == 0
            or len(userRegister.username) == 0
            or len(userRegister.password) == 0
            or len(userRegister.email) == 0)
