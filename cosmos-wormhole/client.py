import httpx
from endpoints import *


class Client:
    def __init__(self, base_url: str = "https://api.xiaoyuzhou.com/v1") -> None:
        self.base_url = base_url
        self.client: httpx.AsyncClient | None = None

    async def login(self) -> None:
        headers = await Login().login()
        self.client = httpx.AsyncClient(base_url=self.base_url, headers=headers)


if __name__ == "__main__":
    import asyncio

    async def main():
        c = Client()
        await c.login()

    asyncio.run(main())
