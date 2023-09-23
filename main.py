import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from src.app.exception_handlers.common import handle_domain_exception
from src.app.routers.note_routers import router as note_router
from src.app.routers.user_routers import router as user_router
from src.core.di.injector import RootContainer
from src.core.errors.base import DomainException

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global container
    print("Starting app")
    container = RootContainer()
    container.wire(modules=[
        "src.app.routers.user_routers",
        "src.app.routers.note_routers",
    ])
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


# @app.middleware("http")
# async def close_db_session(request: Request, call_next):
#     container.session_factory.init()
#     response = await call_next(request)
#     container.session_factory.shutdown()
#     return response


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
