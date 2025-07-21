from typing import AsyncGenerator

import entities

from .base import GetBase, ListBase


class Episode(ListBase[entities.Episode], GetBase[entities.Episode]):
    entity_class = entities.Episode
    endpoint = "/v1/episode"
    list_body = {"order": "desc", "limit": 20}
    get_params_key = "eid"

    def list_by_podcast(
        self, podcast_id: str
    ) -> AsyncGenerator[entities.Episode, None]:
        return self.list({"pid": podcast_id})
