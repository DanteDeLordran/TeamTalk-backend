from pydantic import BaseModel
from hashlib import sha256
from passlib.hash import sha256_crypt

class UserLogin(BaseModel):
    email: str
    password: str

def build_login_dict(userLogin: UserLogin) -> dict:
    login_dict = dict(userLogin)
    login_dict["password"] = sha256(userLogin.password.encode()).hexdigest()
    return login_dict
