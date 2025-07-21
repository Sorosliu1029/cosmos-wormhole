from typing import Any, AsyncGenerator, Type

import httpx


class Base[E]:
    entity_class: Type[E]
    endpoint: str
    list_suffix = "list"
    list_body: dict[str, str | int]

    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client

    def _extract_data(self, json_resp: dict) -> list[dict]:
        return json_resp.get("data", [])

    async def _fetch_entities(
        self, query: dict[str, Any] | None, load_more_key: Any
    ) -> tuple[list[E], Any]:
        resp = await self.client.post(
            f"{self.endpoint}/{self.list_suffix}",
            json=self.list_body
            | (query if query else {})
            | ({"loadMoreKey": load_more_key} if load_more_key else {}),
        )
        json_resp = resp.raise_for_status().json()
        entities = [
            (
                entity
                if isinstance(entity, self.entity_class)
                else self.entity_class(**entity)
            )
            for entity in self._extract_data(json_resp)
        ]
        load_more_key = json_resp.get("loadMoreKey")
        return entities, load_more_key

    async def list(
        self, query: dict[str, Any] | None = None
    ) -> AsyncGenerator[E, None]:
        load_more_key = {}
        while load_more_key is not None:
            entities, load_more_key = await self._fetch_entities(query, load_more_key)
            for entity in entities:
                yield entity
