from datetime import datetime
from typing import Any

from project.apis.crud import create_user, get_user
from project.utils.db import driver
from project.utils.exceptions import UserAlreadyExist, UserNotExist
from project.utils.miscellaneous import get_password_hash, verify_password
from project.utils.schema import (
    LoginPayloadSchema,
    RegisterPayloadSchema,
    Token,
    User,
    UserInDb,
)
from project.utils.tokens import get_access_token

db_driver = driver["driver"]


def add_user_handler(payload: RegisterPayloadSchema) -> User:

    attributes: dict[str, Any] = {
        "username": payload.username,
        "name": payload.name,
        "password": get_password_hash(payload.password),
        "joined": str(datetime.utcnow()),
    }

    with db_driver.session() as sess:
        user: (UserInDb | None) = get_user(UserInDb, payload.username, sess)
        if user:
            raise UserAlreadyExist(payload.username)
        user: User = create_user(parameters=attributes, sess=sess)
    return user


def login_handler(payload: LoginPayloadSchema) -> Token:
    with db_driver.session() as sess:
        user: UserInDb = get_user(UserInDb, payload.username, sess)
    if user and verify_password(payload.password, user.password):
        return Token(**{"access_token": get_access_token(user.username)})
    else:
        raise UserNotExist(payload.username)
