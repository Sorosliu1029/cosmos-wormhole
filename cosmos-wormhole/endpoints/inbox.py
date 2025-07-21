import entities

from .base import ListBase


class Inbox(ListBase[entities.Episode]):
    entity_class = entities.Episode
    endpoint = "/v2/inbox"
    list_body = {"limit": 20}
