from fastapi import APIRouter

from project.apis.auth import router as authRouter
from project.apis.user import router as userRouter

router = APIRouter(prefix="/api/v1")

router.include_router(authRouter)
router.include_router(userRouter)
