import entities

from .base import Base


class Subscription(Base):
    endpoint = "/v1/subscription"
    list_body = {
        "sortBy": "subscribedAt",
        "sortOrder": "desc",
        "limit": 20,
    }
    entity_class = entities.Podcast
