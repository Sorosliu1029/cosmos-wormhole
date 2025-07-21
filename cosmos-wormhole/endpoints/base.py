from typing import Any, AsyncGenerator, Type

import httpx


class Base[E]:
    endpoint: str
    list_body: dict[str, str | int]
    entity_class: Type[E]

    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client

    async def _fetch_entities(
        self, query: dict[str, Any] | None, load_more_key: Any
    ) -> tuple[list[E], Any]:
        resp = await self.client.post(
            f"{self.endpoint}/list",
            json=self.list_body
            | (query if query else {})
            | ({"loadMoreKey": load_more_key} if load_more_key else {}),
        )
        data = resp.raise_for_status().json()
        entities = [self.entity_class(**entity) for entity in data.get("data", [])]
        load_more_key = data.get("loadMoreKey")
        return entities, load_more_key

    async def list(
        self, query: dict[str, Any] | None = None
    ) -> AsyncGenerator[E, None]:
        load_more_key = {}
        while load_more_key is not None:
            entities, load_more_key = await self._fetch_entities(query, load_more_key)
            for entity in entities:
                yield entity
