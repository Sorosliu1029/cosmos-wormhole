import httpx
from endpoints import *
from manager import *


class Client:
    def __init__(self, base_url: str = "https://api.xiaoyuzhoufm.com") -> None:
        self.base_url = base_url
        self.client: httpx.AsyncClient | None = None
        self.token_manager = TokenManager()

    async def login(self) -> None:
        headers = self.token_manager.get_token()
        if not headers:
            headers = await Login().login()
            self.token_manager.save_token(
                access_token=headers["X-Jike-Access-Token"],
                refresh_token=headers["X-Jike-Refresh-Token"],
            )
        self.client = httpx.AsyncClient(base_url=self.base_url, headers=headers)

        asyncio.create_task(self.token_manager.refresh_token(self.client))


if __name__ == "__main__":
    import asyncio

    async def main():
        c = Client()
        await c.login()

        await asyncio.sleep(10)  # Wait for the token refresh task to start

    asyncio.run(main())
