import entities

from .base import ListBase


class Subscription(ListBase[entities.Podcast]):
    entity_class = entities.Podcast
    endpoint = "/v1/subscription"
    list_body = {"sortBy": "subscribedAt", "sortOrder": "desc", "limit": 20}
