"""Модуль запуска приложения."""
import os

import uvicorn
from core.settings import Settings
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv(os.path.join(os.getcwd(), "auth.env"))
    settings = Settings()
    uvicorn.run(
        app="core.app:app",
        host=settings.app_host,
        port=settings.app_port,
        workers=settings.app_uvicorn_workers,
        log_level=settings.app_logging.level.lower(),
        reload=True,
    )
