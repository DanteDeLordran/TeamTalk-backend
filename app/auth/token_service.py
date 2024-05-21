from ..models.dto.user_at_client import UserClient, parse_user_from_mongo_dict
from dotenv import load_dotenv
from jose import jwt
import os
from datetime import datetime, timedelta
from ..db.db_context import db

load_dotenv()

super_secret_key = os.getenv("SUPER_SECRET_KEY")


def get_user_token(user: UserClient) -> str:
    expiration = datetime.now() + timedelta(days=7)

    data_in_token = {
        "username": user.username,
        "email": user.email,
        "expiration": expiration.isoformat()
    }

    token = jwt.encode(claims=data_in_token,
                       key=super_secret_key,
                       algorithm='HS256'
                       )

    return token


def authenticate(token: str) -> UserClient | None:
    claims = jwt.decode(token=token, key=super_secret_key)
    username = claims["username"]
    email = claims["email"]
    expiration = datetime.fromisoformat(claims["expiration"])

    remaining_days = expiration - datetime.now()

    if remaining_days < timedelta(0):
        return None
    
    user_dict = db.users.find_one({"username": username, "email": email})
    if user_dict == None: return None
    user = parse_user_from_mongo_dict(user_dict)
    return user
