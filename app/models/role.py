from pydantic import BaseModel

class Role(BaseModel):
    id: str | None
    name: str
    

def parse_role_from_mongo_dict(role: dict) -> Role:
    role_obj = Role(
        id = role["_id"],
        name = role["name"]
    )
    return role_obj