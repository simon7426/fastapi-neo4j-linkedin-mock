from functools import lru_cache

from passlib.context import CryptContext


@lru_cache
def get_pwd_context() -> CryptContext:
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    ctx: CryptContext = get_pwd_context()
    return ctx.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    ctx: CryptContext = get_pwd_context()
    return ctx.hash(password)
