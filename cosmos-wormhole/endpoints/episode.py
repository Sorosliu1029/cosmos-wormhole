from typing import AsyncGenerator

import entities

from .base import Base


class Episode(Base[entities.Episode]):
    entity_class = entities.Episode
    endpoint = "/v1/episode"
    list_body = {
        "order": "desc",
        "limit": 20,
    }

    def list_by_podcast(
        self, podcast_id: str
    ) -> AsyncGenerator[entities.Episode, None]:
        return self.list({"pid": podcast_id})
