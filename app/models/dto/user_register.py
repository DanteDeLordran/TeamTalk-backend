from pydantic import BaseModel
from hashlib import sha256

class UserRegister(BaseModel):
    name: str
    lastname: str
    username: str
    email: str
    password: str

def build_user_from_register(registration: UserRegister) -> dict:
    registration_dict = dict(registration)
    registration_dict["password"] = sha256(registration.password.encode()).hexdigest()
    return registration_dict