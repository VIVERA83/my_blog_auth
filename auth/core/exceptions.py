"""Обработчик HTTP исключений"""
from core.components import Application, Request
from core.utils import HTTP_EXCEPTION
from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


async def http_exception_handler(request: Request, exc: HTTPException):
    """Перехват исключения, с целью вернуть объект с информацией о документации по приложению."""
    return JSONResponse(
        content={
            "detail": f"{exc.detail}.",
            "message": "See the documentation: "
            + "http://{host}:{port}{uri}".format(
                host=request.app.settings.app_server_host,
                port=request.app.settings.app_port,
                uri=request.app.docs_url,  # noqa
            ),
        },
        status_code=exc.status_code,
    )


async def validation_exception_handler(_: Request, exc: RequestValidationError):
    """Перехват исключения которое возникает при валидации входящий данных в запросе."""
    return JSONResponse(
        content={
            "detail": f"{HTTP_EXCEPTION[status.HTTP_400_BAD_REQUEST]}",
            "message": f"{exc.errors()[0]['msg']}",
        },
        status_code=status.HTTP_400_BAD_REQUEST,
    )


def setup_exception(app: Application):
    """Настройка подключаемый обработчиков исключений."""
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
