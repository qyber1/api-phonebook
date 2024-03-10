from fastapi import APIRouter
from .account_management import auth
from .admin import admin
from .user import user

root = APIRouter()

root.include_router(auth)
root.include_router(admin)
root.include_router(user)
