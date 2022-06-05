from fastapi import APIRouter, status

from project.apis.auth.views import login, register

router = APIRouter(prefix="/auth", tags=["authentication"])

router.add_api_route(
    path="/register",
    endpoint=register,
    status_code=status.HTTP_201_CREATED,
    methods=["POST"],
)
router.add_api_route(
    path="/login", endpoint=login, status_code=status.HTTP_200_OK, methods=["POST"]
)
