from typing import Any, AsyncGenerator

import httpx
from entities import Podcast


class Subscription:
    endpoint = "/v1/subscription"
    list_body = {
        "sortBy": "subscribedAt",
        "sortOrder": "desc",
        "limit": 20,
    }

    def __init__(self, client: httpx.AsyncClient) -> None:
        assert client, "Client must be provided."
        self.client = client

    async def _fetch_podcasts(self, load_more_key: Any) -> tuple[list[Podcast], Any]:
        resp = await self.client.post(
            f"{Subscription.endpoint}/list",
            json=Subscription.list_body
            | ({"loadMoreKey": load_more_key} if load_more_key else {}),
        )
        data = resp.raise_for_status().json()
        podcasts = [Podcast(**podcast) for podcast in data.get("data", [])]
        load_more_key = data.get("loadMoreKey")
        return podcasts, load_more_key

    async def list(self) -> AsyncGenerator[Podcast, None]:
        assert self.client, "Client must be initialized."
        load_more_key = {}
        while load_more_key is not None:
            podcasts, load_more_key = await self._fetch_podcasts(load_more_key)
            for podcast in podcasts:
                yield podcast
