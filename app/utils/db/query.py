from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.models import UserCard

from .tables import User, PhoneBook as PB


async def create_user(session: AsyncSession, user: str, password: str) -> bool:
    try:
        user = User(username=user, password=password)
        session.add(user)
        await session.commit()
        return True
    except Exception as error:
        print(error)
        await session.rollback()
        return False


async def get_user(session: AsyncSession, username: str) -> User | bool:
    try:
        result = await session.execute(select(User.username, User.password, User.role).where(User.username == username))
        return result.fetchall()
    except Exception:
        return False


async def add_usercard(session: AsyncSession, **kwargs) -> dict | bool:
    try:
        usercard = PB(
                            name=kwargs["name"],
                            phone=kwargs["phone"],
                            job_title=kwargs["job_title"],
                            birthday=kwargs["birthday"])
        session.add(usercard)
        await session.commit()
        await session.refresh(usercard)
        return {"status": "ok",
                "user": {
                    "id": usercard.id,
                    "name": usercard.name,
                    "phone": usercard.phone,
                    "job_title": usercard.job_title,
                    "birthday": usercard.birthday
                }}

    except Exception as error:
        print(error)
        await session.rollback()
        return False



async def search_usercard(session: AsyncSession, name: str) -> list[UserCard]:
    all_users = await session.execute(select(PB.id, PB.name,
                                             PB.phone, PB.job_title,
                                             PB.birthday).where(PB.name == name))
    result = all_users.fetchall()
    return [UserCard(**user._mapping) for user in result]



async def update_usercard(session: AsyncSession, user_id: int, **kwargs) -> bool:
    try:
        user = await session.execute(select(PB.name, PB.phone,
                                            PB.job_title, PB.birthday).where(PB.id == user_id))
        user = user.fetchone()
        new_info = dict(user._mapping)
        new_info.update(kwargs)
        await session.execute(update(PB).
                              where(PB.id == user_id).
                              values(**new_info))
        await session.commit()
        return True
    except Exception as error:
        print(error)
        return False


async def delete_usercard(session: AsyncSession, user_id: int) -> None | bool:
    try:
        await session.execute(delete(PB).where(PB.id == user_id))
        await session.commit()
    except Exception as error:
        print(error)
        return False


async def upgrade_profile(session: AsyncSession, username: str) -> None:
    await session.execute(update(User).
                          where(User.username == username).
                          values(role='admin'))
    await session.commit()

