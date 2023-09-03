from core.components import Application
from store.cache.accessor import CacheAccessor
from store.token.accessor import TokenAccessor
from store.user.accessor import UserAccessor
from store.user_manager.manager import UserManager

from tests.app.store.database.postgres import PostgresTest
from tests.app.store.database.redis import RedisAccessorTest
from tests.app.store.ems.ems import EmailMessageServiceTest


class StoreTest:
    def __init__(self, app):
        self.auth = UserAccessor(app)
        self.token = TokenAccessor(app)
        self.auth_manager = UserManager(app)
        self.cache = CacheAccessor(app)
        self.ems = EmailMessageServiceTest(app)


def setup_store_test(app: Application):
    app.postgres = PostgresTest(app)
    app.redis = RedisAccessorTest(app)
    app.store = StoreTest(app)
