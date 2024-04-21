from ..models.user import User
from dotenv import load_dotenv
from jose import jwt
import os
from datetime import datetime, timedelta
from ..db.db_context import db

load_dotenv()

super_secret_key = os.getenv("SUPER_SECRET_KEY")


def get_user_token(user: User) -> str:
    data_in_token = {
        "username": user.username,
        "email": user.email
    }

    expiration = datetime.now() + timedelta(days=7)

    token = jwt.encode(claims=data_in_token,
                       key=super_secret_key,
                       algorithm='HS256',
                       headers={
                           "expiration": expiration.isoformat()
                       })

    return token


def authenticate(token: str) -> User | None:
    pass
