import os

from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_current_user
from app.api.auth.auth_model import CurrentUser
from app.utils.db.database import get_session
from app.utils.db import search_usercard, upgrade_profile
from app.utils.models.models import UserCard

user = APIRouter()



@user.get('/home')
async def user_information(current_user: CurrentUser = Depends(get_current_user)):
    return {"user": current_user.username, "role": current_user.role}


@user.get('/user', dependencies=[Depends(get_current_user)])
async def get_user(name: str, session: AsyncSession = Depends(get_session)) -> dict:
    response: list[UserCard] = await search_usercard(session, name)
    if not response:
        return {"msg": "user not found"}
    return {"items": response}


@user.post('/upgrade_profile')
async def upgrade_user_profile(code: str = Body(), current_user: CurrentUser = Depends(get_current_user),
                          session: AsyncSession = Depends(get_session)):
    if code == os.environ.get("CODE"):
        await upgrade_profile(session, current_user.username)