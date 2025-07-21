from typing import Any, AsyncGenerator, Type

import httpx


def json_to_entity[E](entity_class: Type[E], data: Any) -> E:
    return data if isinstance(data, entity_class) else entity_class(**data)


class ListBase[E]:
    entity_class: Type[E]
    endpoint: str
    list_suffix = "list"
    list_body: dict[str, str | int]

    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client

    def _extract_data(self, json_resp: dict) -> list[Any]:
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
            json_to_entity(self.entity_class, entity_data)
            for entity_data in self._extract_data(json_resp)
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


class GetBase[E]:
    entity_class: Type[E]
    endpoint: str
    get_suffix = "get"
    get_params_key: str

    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client

    async def get(self, entity_id: str) -> E:
        resp = await self.client.get(
            f"{self.endpoint}/{self.get_suffix}",
            params={self.get_params_key: entity_id},
        )
        json_resp = resp.raise_for_status().json()
        entity_data = json_resp.get("data")
        return json_to_entity(self.entity_class, entity_data)
