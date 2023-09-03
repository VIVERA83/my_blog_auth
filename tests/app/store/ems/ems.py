from store.ems.ems import EmailMessageService


class EmailMessageServiceTest(EmailMessageService):
    async def connect(self):
        self.logger.info("Connect EMS")
        pass

    async def disconnect(self):
        pass

    async def send(self, msg):
        pass
