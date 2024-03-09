from fastapi import APIRouter
from .account_management import auth
from .admin import admin
from .user import user
from ..utils.db.database import init_db

root = APIRouter()

root.include_router(auth)
root.include_router(admin)
root.include_router(user)


@root.get('/db')
async def get_db_schema():
    await init_db()
