import entities

from .base import Base


class Episode(Base[entities.Episode]):
    entity_class = entities.Episode
    endpoint = "/v1/episode"
    list_body = {
        "order": "desc",
        "limit": 20,
    }
