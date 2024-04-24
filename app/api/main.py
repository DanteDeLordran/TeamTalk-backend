
from fastapi import APIRouter
from app.api.routes.users_route import users_route

router = APIRouter()

router.include_router( users_route , prefix='/users' , tags=['users'] )