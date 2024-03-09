from fastapi import Depends, HTTPException

from app.api.auth.auth import get_current_user
from app.api.auth.auth_model import CurrentUser


async def is_admin(current_user: CurrentUser = Depends(get_current_user)):
    if current_user.role.value != 'admin':
        raise HTTPException(status_code=403, detail='Permission denied')
    return True