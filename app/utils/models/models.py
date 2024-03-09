import datetime
import re

from pydantic import BaseModel, field_validator


class RegistrationForm(BaseModel):
    username: str
    password: str


class UserCard(BaseModel):
    id: int
    name: str
    phone: str
    job_title: str
    birthday: datetime.date


class CreateUserCard(BaseModel):
    name: str
    phone: str
    job_title: str
    birthday: datetime.date


    @field_validator('phone')
    @classmethod
    def check_phone(cls, value) -> str:
        phone_pattern = '^(\+7|8)?\s?(\d{3}[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}|\d{10})$'
        if re.search(phone_pattern, value):
            return value


class UpdateUserCard(BaseModel):
    id: int
    fields: dict


class DeleteUserCard(BaseModel):
    id: int
