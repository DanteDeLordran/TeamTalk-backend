from pydantic import BaseModel

class Role(BaseModel):
    id: str | None
    name: str
    

def parse_role_from_mongo_dict(role: dict) -> Role:
    role_obj = Role()
    role_obj.id = role["_id"]
    role_obj .name = role["name"]
    return role_obj