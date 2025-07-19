import httpx
from endpoints import *
from managers import *


class Client:
    def __init__(self, base_url: str = "https://api.xiaoyuzhoufm.com") -> None:
        self.base_url = base_url
        self.client: httpx.AsyncClient | None = None
        self.token_manager = TokenManager()
        self.subscription: Subscription

    async def login(self) -> None:
        headers = self.token_manager.get_token()
        # first time or no token stored, try to login
        if not headers:
            headers = await Login().login()
            self.token_manager.save_token(
                access_token=headers["X-Jike-Access-Token"],
                refresh_token=headers["X-Jike-Refresh-Token"],
            )

        self.client = httpx.AsyncClient(base_url=self.base_url, headers=headers)
        # refresh tokens in case of access token expired
        if headers:
            access_token, refresh_token = await self.token_manager.refresh_token(
                self.client
            )
            self.client.headers.update(
                {
                    "X-Jike-Access-Token": access_token,
                    "X-Jike-Refresh-Token": refresh_token,
                }
            )

        self.after_login()

    def after_login(self) -> None:
        assert self.client, "Client must be initialized."
        asyncio.create_task(
            self.token_manager.periodic_refresh_token(self.client, 60 * 20)
        )
        self.subscription = Subscription(self.client)


if __name__ == "__main__":
    import asyncio

    async def main():
        c = Client()
        await c.login()

        async for podcast in c.subscription.list():
            print(podcast)

    asyncio.run(main())
