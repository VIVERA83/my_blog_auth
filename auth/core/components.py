"""Переназначенные компоненты Fast-Api."""
import logging
from typing import Any, Optional

from base.type_hint import Public_access, Url
from core.settings import Settings
from core.utils import METHODS, PUBLIC_ACCESS, Token
from fastapi import FastAPI
from fastapi import Request as FastAPIRequest
from fastapi.openapi.utils import get_openapi
from starlette.datastructures import State
from store.database.postgres import Postgres
from store.database.redis import RedisAccessor
from store.store import Store


class Application(FastAPI):
    """Application главный класс.

    Описываем сервисы, которые будут использоваться в приложении.
    Так же это нужно для корректной подсказки IDE.
    """

    settings: Settings
    store: Store
    redis: RedisAccessor
    postgres: Postgres
    logger: logging.Logger
    docs_url: Url
    public_access: Public_access

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._create_public_urls()
        self.public_access.extend(PUBLIC_ACCESS)
        self.openapi = self._custom_openapi

    def _create_public_urls(self):
        self.public_access = []
        self.public_access.append(
            (
                self.docs_url,
                "GET",
            )
        )
        self.public_access.append(
            (
                self.redoc_url,
                "GET",
            )
        )
        self.public_access.append(
            (
                self.openapi_url,
                "GET",
            )
        )
        self.public_access.append(
            (
                self.swagger_ui_oauth2_redirect_url,
                "GET",
            )
        )

    def _custom_openapi(self) -> dict[str, Any]:
        """Обновления схемы в Openapi.

        Добавление в закрытые методы HTTPBearer.

        Returns:
            dict: Dictionary openapi schema
        """

        if self.openapi_schema:
            return self.openapi_schema
        openapi_schema = get_openapi(
            title=self.settings.app_name,
            description=self.settings.app_description,
            routes=self.routes,
            version=self.settings.app_version,
        )

        for key, path in openapi_schema["paths"].items():
            is_free, free_method = self._is_free(key)

            if not is_free:
                self._add_security(free_method, path)

        self.openapi_schema = openapi_schema
        return self.openapi_schema

    def _is_free(self, url: str):
        assert self.public_access is not None
        is_free = False
        free_method = None
        for f_p, f_m in self.public_access:
            if url == f_p:
                is_free = True
                free_method = f_m
        return is_free, free_method

    @staticmethod
    def _add_security(name: Optional[str], path: dict):
        """Add a security."""

        for method in METHODS:
            if method.upper() != name and path.get(method.lower()):
                path[method.lower()]["security"] = [{"HTTPBearer": []}]


class Request(FastAPIRequest):
    """Переопределения Request.

    Для корректной подсказки IDE по методам `Application`."""

    @property
    def state(self) -> "CustomState":
        """Для корректной подсказки IDE по методам `Request`.

        Returns:
             CustomState: state
        """
        return self._state


class CustomState(State):
    """Переопределения State.

    Для корректной подсказки IDE по методам `Request`.
    """

    token: Optional["Token"]
    user_id: Optional[str] = None
