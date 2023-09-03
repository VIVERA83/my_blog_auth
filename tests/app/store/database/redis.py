from store.database.redis import RedisAccessor


class RedisAccessorTest(RedisAccessor):
    async def disconnect(self):
        await self.connector.flushdb()
        await super().disconnect()
