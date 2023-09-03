from store.database.postgres import Postgres


class PostgresTest(Postgres):
    async def connect(self):
        """Configuring the connection to the database."""
        await super().connect()

    async def disconnect(self):
        await super().disconnect()
