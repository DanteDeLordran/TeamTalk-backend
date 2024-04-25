from .role_definition import RoleDefinition, Field

class Admin(RoleDefinition):
    rolename: str = "Admin"

    # basic permissions for social interaction
    can_send_messages: bool = True
    can_delete_messages: bool = True
    can_modify_message: bool = True
    can_send_invitation: bool = True
    can_revoke_invitation: bool = True

    # high level permissions
    can_delete_others_messages: bool = True
    can_kick_others: bool = True
    can_ban_others: bool = True
    can_assign_roles: bool = True
    can_manage_group: bool = True
    can_delete_group: bool = True
    can_accept_participants: bool = True
 