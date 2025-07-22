from typing import Any, override

from .. import entities
from .base import ListBase


class History(ListBase[entities.Episode]):
    entity_class = entities.Episode
    endpoint = "/v1/episode-played"
    list_suffix = "list-history"

    @override
    def _extract_data(self, json_resp: dict) -> list[Any]:
        return list(filter(None, [d.get("episode") for d in json_resp.get("data", [])]))
