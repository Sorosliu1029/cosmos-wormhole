import asyncio

import httpx
import qrcode

from ..managers import Token


class Login:
    def __init__(self) -> None:
        self.client = httpx.AsyncClient(
            base_url="https://podcaster-api.xiaoyuzhoufm.com/v1/auth"
        )
        self.id = None

    async def __get_login_url(self) -> str:
        resp = await self.client.post(
            "/qrcode/create",
            json={"clientId": "podcaster-platform"},
            headers={"X-Midway-App-Id": "v6worU4NnWyL"},
        )
        data = resp.raise_for_status().json()
        self.id, url = data.values()
        return url

    async def __check_login(self) -> tuple[str, str] | None:
        resp = await self.client.post("/qrcode/login", json={"id": self.id})
        data = resp.raise_for_status().json()
        if data["status"] != "USED":
            if data["status"] == "SCANNED":
                print("二维码已被扫描，请在小宇宙App中确认登录。")
            return None

        access_token = resp.headers.get(Token.access_key)
        refresh_token = resp.headers.get(Token.refresh_key)
        assert access_token and refresh_token, "Login failed, tokens not found."
        return (access_token, refresh_token)

    def __show_qr_code(self, url: str) -> None:
        qr = qrcode.QRCode()
        qr.add_data(url)
        print("打开小宇宙App，使用「发现」Tab - 搜索框右侧「扫一扫」登录")
        print("PS: 小宇宙会提示登录「小宇宙主播后台」。主播后台和主App账号互通")
        qr.print_ascii()

    async def login(self) -> tuple[str, str]:
        url = await self.__get_login_url()
        self.__show_qr_code(url)

        headers = await self.__check_login()
        while headers is None:
            await asyncio.sleep(1)
            headers = await self.__check_login()

        print("登录成功！")
        await self.client.aclose()
        return headers
