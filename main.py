import logging
import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from setup_infra import setup_infra
from src.app.exception_handlers.common import handle_domain_exception
from src.app.routers.note_routers import router as note_router
from src.app.routers.user_routers import router as user_router
from src.core.di.injector import RootContainer
from src.core.errors.base import DomainException
from src.core.settings import Settings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


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
    setup_infra()
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

# cors middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
