import datetime
from enum import Enum
from sqlalchemy import String, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Permissions(Enum):
    default = 'default'
    admin = 'admin'


class BaseModel(DeclarativeBase):
    pass


class PhoneBook(BaseModel):
    __tablename__ = "Phonebook"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60))
    phone: Mapped[str] = mapped_column(String(60))
    job_title: Mapped[str] = mapped_column(String(60))
    birthday: Mapped[datetime.date] = mapped_column(Date)


class User(BaseModel):
    __tablename__ = 'User'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    username: Mapped[str] = mapped_column(String(60), unique=True)
    password: Mapped[str] = mapped_column(String(78))
    role: Mapped[Permissions] = mapped_column(nullable=False, default=Permissions.default)
