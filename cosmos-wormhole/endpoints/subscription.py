import entities

from .base import Base


class Subscription(Base[entities.Podcast]):
    entity_class = entities.Podcast
    endpoint = "/v1/subscription"
    list_body = {
        "sortBy": "subscribedAt",
        "sortOrder": "desc",
        "limit": 20,
    }
