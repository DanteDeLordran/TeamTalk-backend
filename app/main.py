from fastapi import FastAPI
from app.api.main import router

app = FastAPI()

app.include_router(router)