import httpx
from endpoints import *
from managers import *


class Client:
    # TODO: read version
    user_agent = "CosmosWormhole/0.0.1"

    def __init__(self, base_url: str = "https://api.xiaoyuzhoufm.com") -> None:
        self.client = httpx.AsyncClient(
            base_url=base_url, headers={"user-agent": self.user_agent}
        )
        self.token_manager = TokenManager()
        self.token_update_queue = asyncio.Queue(2)
        self.token_update_producer: asyncio.Task
        self.token_update_consumer: asyncio.Task
        self.subscription: Subscription
        self.episode: Episode

    def _update_token(self, access_token: str, refresh_token: str) -> None:
        self.token_manager.save_token(
            access_token=access_token, refresh_token=refresh_token
        )
        self.client.headers.update(
            {Token.access_key: access_token, Token.refresh_key: refresh_token}
        )
        print(self.client.headers)

    async def login(self) -> None:
        headers = self.token_manager.get_token()

        if not headers:  # first time or no token stored, try to login
            access_token, refresh_token = await Login().login()
            self._update_token(access_token, refresh_token)
        else:  # refresh tokens in case of access token expired
            self.client.headers.update(headers)
            access_token, refresh_token = await self.token_manager.refresh_token(
                self.client
            )
            self._update_token(access_token, refresh_token)

        self.after_login()

    def after_login(self) -> None:
        self.token_update_producer = asyncio.create_task(
            self.token_manager.periodic_refresh_token(
                self.client, 60 * 1, self.token_update_queue
            )  # every 20 minutes
        )
        self.token_update_consumer = asyncio.create_task(self._listen_on_token_update())
        self.subscription = Subscription(self.client)
        self.episode = Episode(self.client)

    async def _listen_on_token_update(self) -> None:
        while True:
            access_token, refresh_token = await self.token_update_queue.get()
            self._update_token(access_token, refresh_token)
            self.token_update_queue.task_done()


if __name__ == "__main__":
    import asyncio

    async def main():
        c = Client()
        await c.login()

        async for podcast in c.subscription.list():
            print(podcast)
            async for episode in c.episode.list({"pid": podcast.id}):
                print(f"\t{episode}")
            break

        await asyncio.sleep(60 * 5)

    asyncio.run(main())
