import logging
from datetime import datetime, timedelta
from typing import Any

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from project.config import Settings, get_settings
from project.utils.exceptions import INVALID_TOKEN_EXCEPTION, TOKEN_EXPIRED_EXCEPTION

log = logging.getLogger("uvicorn")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_access_token(username: str) -> Settings:
    settings = get_settings()
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(seconds=settings.expiration),
    }
    return jwt.encode(payload=payload, key=settings.secret, algorithm="HS256")


def validate_token(
    token: str = Depends(oauth2_scheme), settings: Settings = Depends(get_settings)
) -> dict[str, Any]:
    try:
        payload: dict[str, Any] = jwt.decode(
            token, key=settings.secret, algorithms=["HS256"]
        )
        return payload
    except jwt.InvalidSignatureError:
        raise INVALID_TOKEN_EXCEPTION
    except jwt.ExpiredSignatureError:
        raise TOKEN_EXPIRED_EXCEPTION
    except Exception as e:
        log.info(e)
        raise INVALID_TOKEN_EXCEPTION
