import logging
import os
import time
from contextlib import asynccontextmanager
from typing import Any

import requests
from fastapi import Body, FastAPI, Request
from pydantic import Json

from src.app.exception_handlers.common import handle_domain_exception
from src.app.routers.note_routers import router as note_router
from src.app.routers.user_routers import router as user_router
from src.core.di.injector import RootContainer
from src.core.errors.base import DomainException
from src.core.settings import Settings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Set AWS access key and secret key as environment variables
os.environ['AWS_ACCESS_KEY_ID'] = 'test'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'test'
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    global container
    print("Starting app")
    settings = Settings.cached()
    container = RootContainer()
    container.config.from_dict(
        settings.model_dump()
    )
    container.wire(modules=[
        "src.app.routers.user_routers",
        "src.app.routers.note_routers",
    ])
    topic = f"{settings.s3_bucket_name}-topic"
    container.sns_provider().configure_s3(
        bucket_name=settings.s3_bucket_name,
        topic=topic
    )
    container.sns_provider().subscribe_sns_with_endpoint(
        topic=topic,
        endpoint="http://host.docker.internal:8000/message/"
    )
    # Bind container to app
    setattr(app, "container", container)
    yield
    print("Stopping app")


def init_app():
    app = FastAPI(lifespan=lifespan)

    api_version = "v0"
    app.include_router(user_router, prefix=f"/api/{api_version}")
    app.include_router(note_router, prefix=f"/api/{api_version}")
    return app


app = init_app()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.exception_handler(DomainException)
def handler(request: Request, exc: DomainException):
    return handle_domain_exception(request, exc)


@app.post("/message/")
def handle_sns_message(message: Json = Body(...)):
    type = message['Type']
    match type:
        case "SubscriptionConfirmation":
            sub_url = message["SubscribeURL"]
            sub_url = sub_url.replace("localhost", "host.docker.internal")
            response = requests.get(sub_url)
            print("Subscription Confirmation: ", response)

    logger.info(f"Received message {message}")
    return {"message": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
