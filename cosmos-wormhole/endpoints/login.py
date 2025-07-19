import asyncio

import httpx
import qrcode


class Login:
    def __init__(self) -> None:
        self.client = httpx.AsyncClient(
            base_url="https://podcaster-api.xiaoyuzhoufm.com/v1/auth"
        )
        self.id = None

    async def _get_login_url(self) -> str:
        resp = await self.client.post(
            "/qrcode/create",
            json={"clientId": "podcaster-platform"},
            headers={"X-Midway-App-Id": "v6worU4NnWyL"},
        )
        data = resp.raise_for_status().json()
        self.id, url = data.values()
        return url

    async def _check_login(self) -> httpx.Headers | None:
        resp = await self.client.post("/qrcode/login", json={"id": self.id})
        data = resp.raise_for_status().json()
        if data["status"] != "USED":
            return None

        access_token = resp.headers.get("X-Jike-Access-Token")
        refresh_token = resp.headers.get("X-Jike-Refresh-Token")
        assert access_token and refresh_token, "Login failed, tokens not found."
        return httpx.Headers(
            {"X-Jike-Access-Token": access_token, "X-Jike-Refresh-Token": refresh_token}
        )

    async def login(self) -> httpx.Headers:
        url = await self._get_login_url()
        qr = qrcode.QRCode()
        qr.add_data(url)
        qr.print_tty()

        headers = await self._check_login()
        while not headers:
            await asyncio.sleep(1)
            headers = await self._check_login()

        await self.client.aclose()
        return headers
