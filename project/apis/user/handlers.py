from typing import List

from project.apis.crud import (
    accept_friend_request,
    already_friend_validation,
    delete_follow,
    follow_user,
    get_requests,
    get_user,
    list_friends,
    send_request_validation,
)
from project.utils.db import driver
from project.utils.exceptions import (
    BAD_REQUEST_EXCEPTION,
    AlreadyFriend,
    AlreadySentRequest,
    NoRequestSent,
)
from project.utils.schema import BasicResponse, RelationShipSchema, User

db_driver = driver["driver"]


def current_user_handler(username: str) -> User:
    with db_driver.session() as sess:
        user: User = get_user(User, username, sess)
    return user


def get_user_info_handler(username: str) -> User:
    with db_driver.session() as sess:
        user: User = get_user(User, username, sess)
    return user


def send_friend_request_handler(user1: str, user2: str) -> RelationShipSchema:
    with db_driver.session() as sess:
        _: User = get_user(User, user2, sess)
        if send_request_validation(user1, user2, sess):
            raise AlreadySentRequest(user2)
        if already_friend_validation(user1, user2, sess):
            raise AlreadyFriend(user2)

        relationshipData: RelationShipSchema = follow_user(
            user1=user1,
            user2=user2,
            sess=sess,
        )
    return relationshipData


def get_requests_handler(username: str) -> List[User]:
    with db_driver.session() as sess:
        userList: List[User] | None = get_requests(username, sess)
    return userList if userList else []


def accept_requests_handler(user1: str, user2: str) -> RelationShipSchema:
    with db_driver.session() as sess:
        _: User = get_user(User, user2, sess)
        if not send_request_validation(user2, user1, sess):
            raise NoRequestSent(user2)
        if already_friend_validation(user1, user2, sess):
            raise AlreadyFriend(user2)
        relationshipData: RelationShipSchema = accept_friend_request(
            user1=user1, user2=user2, sess=sess
        )
    return relationshipData


def reject_request_handler(user1: str, user2: str) -> BasicResponse:
    with db_driver.session() as sess:
        _: User = get_user(User, user2, sess)
        if not send_request_validation(user2, user1, sess):
            raise NoRequestSent(user2)
        if already_friend_validation(user1, user2, sess):
            raise AlreadyFriend(user2)
        if delete_follow(user1, user2, sess):
            responseObject = {"message": "Request deleted successfully."}
            return responseObject
        else:
            raise BAD_REQUEST_EXCEPTION


def list_friends_handler(user: str) -> List[User]:
    with db_driver.session() as sess:
        return list_friends(user, sess)
