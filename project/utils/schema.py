from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    username: str
    name: Optional[str]
    joined: Optional[datetime]


class UserInDb(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str


class TokenData(BaseModel):
    username: str


# * Payload Schemas *#


class RegisterPayloadSchema(BaseModel):
    username: str
    name: Optional[str]
    password: str


class LoginPayloadSchema(BaseModel):
    username: str
    password: str


class RelationShipSchema(BaseModel):
    created_at: datetime


class BasicResponse(BaseModel):
    message: str
