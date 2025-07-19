import asyncio
import json
import os
import time

import httpx


class TokenManager:
    def __init__(self):
        self.token_path = os.path.join(
            os.path.expanduser("~"), ".local", "state", "cosmos-wormhole", "token.json"
        )

    def get_token(self) -> dict:
        if not os.path.exists(self.token_path):
            return {}

        with open(self.token_path, "r", encoding="utf-8") as f:
            tokens = json.load(f)
        expires_at = tokens.get("expiresAt")
        if expires_at and expires_at < time.time():
            return {}

        access_token = tokens.get("accessToken")
        refresh_token = tokens.get("refreshToken")
        assert access_token and refresh_token, "Tokens not found."
        return {
            "X-Jike-Access-Token": access_token,
            "X-Jike-Refresh-Token": refresh_token,
        }

    def save_token(self, access_token: str, refresh_token: str) -> None:
        tokens = {
            "accessToken": access_token,
            "refreshToken": refresh_token,
            "expiresAt": int(time.time()) + 60 * 60 * 24 * 30,  # 30 days
        }
        os.makedirs(os.path.dirname(self.token_path), exist_ok=True)
        with open(self.token_path, "w", encoding="utf-8") as f:
            json.dump(tokens, f, ensure_ascii=False, indent=4)

    def delete_token(self) -> None:
        if os.path.exists(self.token_path):
            os.remove(self.token_path)

    async def refresh_token(self, client: httpx.AsyncClient) -> tuple[str, str]:
        resp = await client.post("/app_auth_tokens.refresh")
        access_token = resp.headers.get("X-Jike-Access-Token")
        refresh_token = resp.headers.get("X-Jike-Refresh-Token")
        return access_token, refresh_token

    async def periodic_refresh_token(
        self, client: httpx.AsyncClient, interval: int
    ) -> None:
        if not os.path.exists(self.token_path):
            return
        while True:
            await asyncio.sleep(interval)
            access_token, refresh_token = await self.refresh_token(client)
            if access_token and refresh_token:
                # TODO: notify client to update its headers
                self.save_token(
                    access_token=access_token,
                    refresh_token=refresh_token,
                )
