from core.components import Application
from core.exceptions import setup_exception
from core.logger import setup_logging
from core.middelware import setup_middleware
from core.routes import setup_routes
from core.settings import Settings

from tests.app.store.store import setup_store_test


def setup_app_test() -> Application:
    app = Application()
    app.settings = Settings()
    setup_logging(app)
    setup_store_test(app)
    setup_middleware(app)
    setup_exception(app)
    setup_routes(app)
    return app
