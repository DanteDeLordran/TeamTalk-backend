from .role_definition import RoleDefinition

class NormalParticipant(RoleDefinition):
    rolename: str = "Participant"

    # basic permissions for social interaction
    can_send_messages = True
    can_delete_messages = True
    can_modify_messages = True
    can_send_invitation = True
 