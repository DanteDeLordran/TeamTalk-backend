from pydantic import BaseModel, Field


class RoleDefinition(BaseModel):
    rolename: str = Field(default="Unnamed Role")

    # basic permissions for social interaction
    can_send_messages: bool = False
    can_delete_messages: bool = False
    can_modify_messages: bool = False
    can_send_invitation: bool = False
    can_revoke_invitation: bool = False

    # high level permissions
    can_delete_others_messages: bool = False
    can_kick_others: bool = False
    can_ban_others: bool = False
    can_assign_roles: bool = False
    can_manage_group: bool = False
    can_delete_group: bool = False
    can_accept_participants: bool = False


def parse_role_from_mongo_dict(role: dict) -> RoleDefinition:
    role_obj = RoleDefinition(
        rolename=role["rolename"],
        can_send_messages=role["can_send_messages"],
        can_delete_messages=role["can_delete_messages"],
        can_modify_messages=role["can_modify_messages"],
        can_send_invitation=role["can_send_invitation"],
        can_revoke_invitation=role["can_revoke_invitation"],
        can_delete_others_messages=role["can_delete_others_messages"],
        can_kick_others=role["can_kick_others"],
        can_ban_others=role["can_ban_others"],
        can_assign_roles=role["can_assign_roles"],
        can_manage_group=role["can_manage_group"],
        can_delete_group=role["can_delete_group"],
        can_accept_participants=role["can_accept_participants"]
    )

    return role_obj
