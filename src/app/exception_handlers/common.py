from fastapi import Request
from fastapi.responses import JSONResponse

from src.core.errors.base import DomainException


def handle_domain_exception(request: Request, exc: DomainException):
    status_code: int = 400

    match exc:
        case ResourceNotFoundException:
            status_code = 404

    return JSONResponse(
        status_code=status_code,
        content={
            "message": exc.message,
            "code": exc.code,
        },
    )
