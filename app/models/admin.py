from .role_definition import RoleDefinition

class Admin(RoleDefinition):
    rolename: str = "Admin"

    # basic permissions for social interaction
    can_send_messages = True
    can_delete_messages = True
    can_modify_message = True
    can_send_invitation = True
    can_revoke_invitation = True

    # high level permissions
    can_delete_others_messages = True
    can_kick_others = True
    can_ban_others = True
    can_assign_roles = True
    can_manage_group = True
    can_delete_group = True
    can_accept_participants = True
 