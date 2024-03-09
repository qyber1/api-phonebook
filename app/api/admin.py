
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.depends.dependencies import is_admin
from app.utils.db.database import get_session
from app.utils.models import CreateUserCard as Create, \
                                    UpdateUserCard as Update, \
                                    DeleteUserCard as Delete

from app.utils.db import add_usercard, update_usercard, delete_usercard

admin = APIRouter(prefix='/admin',
                  dependencies=[Depends(is_admin)])



@admin.post('/user')
async def create_user_card(user: Create, session: AsyncSession = Depends(get_session)) -> dict:
    response: dict = await add_usercard(session, **user.model_dump(mode='python'))
    return response


@admin.patch('/user')
async def update_user_card(user: Update, session: AsyncSession = Depends(get_session)):
    """
    Параметры при запросе в поле fields вводятся в виде ключ-значение:\n
        name: ФИО человека в карточке
        phone: Номер телефона
        job_title: Занимаемая должность
        birthday: День рождения
    """
    response = await update_usercard(session, user.id, **user.fields)
    if not response:
        raise HTTPException(status_code=400, detail='Invalid fields for update')
    return {"status": "success"}


@admin.delete('/user')
async def delete_user_card(user_id: Delete,  session: AsyncSession = Depends(get_session)):
    response = await delete_usercard(session, user_id)
    if not response:
        raise HTTPException(status_code=400, detail='Invalid ID')
    return {"status": "success"}

