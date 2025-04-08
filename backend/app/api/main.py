# 3rd party imports
from fastapi import APIRouter
# local modules
from app.api.routes import health
from app.api.routes.v1 import login

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(login.router, prefix="/v1")
