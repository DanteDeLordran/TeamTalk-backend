
from fastapi import APIRouter
from app.api.routes.users_route import users_route
from app.api.routes.group_route import group_route
from app.api.routes.channel_route import channel_route
from app.api.routes.messages_route import messages_route

router = APIRouter()

router.include_router( users_route, prefix='/users', tags=['users'] )
router.include_router( group_route, prefix='/groups', tags=['groups'] )
router.include_router( channel_route, prefix='/channels', tags=['channels'] )
router.include_router( messages_route, prefix='/messages', tags=['messages'] )