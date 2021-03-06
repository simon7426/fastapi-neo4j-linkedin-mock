from typing import Any, List

from fastapi import Depends

from project.apis.user.handlers import (
    accept_requests_handler,
    current_user_handler,
    distance_user_handler,
    get_requests_handler,
    get_user_info_handler,
    list_friends_handler,
    reject_request_handler,
    send_friend_request_handler,
    unfriend_user_handler,
)
from project.utils.exceptions import BAD_REQUEST_EXCEPTION
from project.utils.schema import BasicResponse, RelationShipSchema, User
from project.utils.tokens import validate_token


async def current_user(user: dict[str, Any] = Depends(validate_token)) -> User:
    return current_user_handler(user["sub"])


async def get_user_info(username: str, _: dict[str, Any] = Depends(validate_token)):
    return get_user_info_handler(username)


async def send_friend_request(
    username: str, owner: dict[str, Any] = Depends(validate_token)
) -> RelationShipSchema:
    if username == owner["sub"]:
        raise BAD_REQUEST_EXCEPTION
    return send_friend_request_handler(user1=owner["sub"], user2=username)


async def get_friend_requests(
    owner: dict[str, Any] = Depends(validate_token)
) -> List[User]:
    return get_requests_handler(owner["sub"])


async def accept_request(
    username: str, owner: dict[str, Any] = Depends(validate_token)
) -> RelationShipSchema:
    return accept_requests_handler(owner["sub"], username)


async def reject_request(
    username: str, owner: dict[str, Any] = Depends(validate_token)
) -> BasicResponse:
    return reject_request_handler(owner["sub"], username)


async def list_friends(owner: dict[str, Any] = Depends(validate_token)) -> List[User]:
    return list_friends_handler(owner["sub"])


async def unfriend_user(
    username: str, owner: dict[str, Any] = Depends(validate_token)
) -> BasicResponse:
    return unfriend_user_handler(owner["sub"], username)


async def distance_user(
    username: str, owner: dict[str, Any] = Depends(validate_token)
) -> BasicResponse:
    return distance_user_handler(owner["sub"], username)
