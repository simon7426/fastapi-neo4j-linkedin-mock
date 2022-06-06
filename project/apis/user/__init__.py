from fastapi import APIRouter, status

from project.apis.user.views import (
    accept_request,
    current_user,
    get_friend_requests,
    get_user_info,
    list_friends,
    reject_request,
    send_friend_request,
)

router = APIRouter(prefix="/user", tags=["user"])

router.add_api_route(
    "", endpoint=current_user, status_code=status.HTTP_200_OK, methods=["GET"]
)
router.add_api_route(
    "/info/{username}",
    endpoint=get_user_info,
    status_code=status.HTTP_200_OK,
    methods=["GET"],
)
router.add_api_route(
    "/follow/{username}",
    endpoint=send_friend_request,
    status_code=status.HTTP_200_OK,
    methods=["GET"],
)
router.add_api_route(
    "/accept/{username}",
    endpoint=accept_request,
    status_code=status.HTTP_200_OK,
    methods=["GET"],
)
router.add_api_route(
    "/requests",
    endpoint=get_friend_requests,
    status_code=status.HTTP_200_OK,
    methods=["GET"],
)
router.add_api_route(
    "/reject/{username}",
    endpoint=reject_request,
    status_code=status.HTTP_200_OK,
    methods=["GET"],
)
router.add_api_route(
    "/friends",
    endpoint=list_friends,
    status_code=status.HTTP_200_OK,
    methods=["GET"],
)
