from pydantic import BaseModel


class UserClient(BaseModel):
    id: str | None
    name: str
    lastname: str
    username: str
    email: str


def parse_user_from_mongo_dict(user: dict) -> UserClient:
    user_obj = UserClient(
        id = str(user["_id"]),
        name = user["name"],
        lastname = user["lastname"],
        username = user["username"],
        email = user["email"]
    )
    return user_obj
