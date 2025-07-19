import entities

from .base import Base


class Episode(Base):
    endpoint = "/v1/episode"
    list_body = {
        "order": "desc",
        "limit": 20,
    }
    entity_class = entities.Episode
