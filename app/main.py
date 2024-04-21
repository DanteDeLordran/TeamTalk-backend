from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .api.routes.users_route import users_route

app = FastAPI()

app.include_router(prefix="/users", router=users_route)