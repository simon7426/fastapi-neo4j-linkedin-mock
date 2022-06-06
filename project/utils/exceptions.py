from urllib.request import Request

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

INVALID_TOKEN_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Please Provide a valid authentication token.",
)
TOKEN_EXPIRED_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Token signature expired."
)
BAD_REQUEST_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request."
)


class UserNotExist(Exception):
    def __init__(self, username: str) -> None:
        self.username = username


class UserAlreadyExist(Exception):
    def __init__(self, username: str) -> None:
        self.username = username


class AlreadySentRequest(Exception):
    def __init__(self, username: str) -> None:
        self.username = username


class AlreadyFriend(Exception):
    def __init__(self, username: str) -> None:
        self.username = username


class NoRequestSent(Exception):
    def __init__(self, username: str) -> None:
        self.username = username


class NotFriend(Exception):
    def __init__(self, username: str) -> None:
        self.username = username


async def user_not_exists_exception_handler(request: Request, exc: UserNotExist):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detatil": f"User {exc.username} does not exists."},
    )


async def user_already_exists_exception_handler(request: Request, exc: UserNotExist):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detatil": f"User {exc.username} already exists."},
    )


async def already_sent_request_exception_handler(
    request: Request, exc: AlreadySentRequest
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detatil": f"Already sent request to User {exc.username}."},
    )


async def already_friend_exception_handler(request: Request, exc: AlreadyFriend):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detatil": f"Already friends with User {exc.username}."},
    )


async def no_request_sent_exception_handler(request: Request, exc: AlreadyFriend):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detatil": f"User {exc.username} do not have any pending requests with you."
        },
    )


async def not_friend_exception_handler(request: Request, exc: NotFriend):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": f"User {exc.username} is not a friend."},
    )
