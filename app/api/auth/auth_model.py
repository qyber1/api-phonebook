from pydantic import BaseModel

from app.utils.db.tables import Permissions


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class CurrentUser(BaseModel):
    username: str
    role: Permissions
