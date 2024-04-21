from pydantic import BaseModel


class User(BaseModel):
    id: str | None
    name: str
    lastname: str
    username: str
    password: str
    email: str


def parse_user_from_mongo_dict(user: dict) -> User:
    user_obj = User(
        id = str(user["_id"]),
        name = user["name"],
        lastname = user["lastname"],
        username = user["username"],
        password = user["password"],
        email = user["email"]
    )
    return user_obj
