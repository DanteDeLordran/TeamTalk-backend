from .role_definition import RoleDefinition, Field

class NormalParticipant(RoleDefinition):
    rolename: str = "Participant"

    # basic permissions for social interaction
    can_send_messages: bool = True
    can_delete_messages: bool = True
    can_modify_messages: bool = True
    can_send_invitation: bool = True
 