from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import authenticate_user, create_access_token
from app.api.auth.auth_model import Token
from app.api.auth.hasher import PasswordManager
from app.utils.db.database import get_session
from app.utils.db import create_user
from app.utils.models import RegistrationForm

auth = APIRouter()


@auth.post('/register')
async def registration_user(user: RegistrationForm, session: AsyncSession = Depends(get_session)) -> dict:
    hashed_password = PasswordManager.hash(user.password)
    flag = await create_user(session, user.username, hashed_password)
    if flag:
        return {"response": "Success"}
    return {"response": "Error! Invalid password or email"}


@auth.post('/login')
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                     session: AsyncSession = Depends(get_session)) -> Token:
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": user.username})
    return Token(access_token=access_token, token_type='bearer')