import logging

from fastapi import FastAPI

from project.apis import alive, router
from project.utils.exceptions import (
    AlreadyFriend,
    AlreadySentRequest,
    UserAlreadyExist,
    UserNotExist,
    already_friend_exception_handler,
    already_sent_request_exception_handler,
    user_already_exists_exception_handler,
    user_not_exists_exception_handler,
)

log = logging.getLogger("uvicorn")


def create_app() -> FastAPI:
    app = FastAPI()

    # * Adding Routers to app *#
    app.include_router(alive.router)
    app.include_router(router)

    # * Adding Exception Handlers *#
    app.add_exception_handler(UserNotExist, user_not_exists_exception_handler)
    app.add_exception_handler(UserAlreadyExist, user_already_exists_exception_handler)
    app.add_exception_handler(AlreadyFriend, already_friend_exception_handler)
    app.add_exception_handler(
        AlreadySentRequest, already_sent_request_exception_handler
    )

    return app


app = create_app()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
