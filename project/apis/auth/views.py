import logging

from project.apis.auth.handlers import add_user_handler, login_handler
from project.utils.schema import LoginPayloadSchema, RegisterPayloadSchema, Token, User

log = logging.getLogger("uvicorn")


async def register(payload: RegisterPayloadSchema) -> User:
    return add_user_handler(payload)


async def login(payload: LoginPayloadSchema) -> Token:
    return login_handler(payload)
