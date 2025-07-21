import entities

from .base import Base


class Comment(Base[entities.Comment]):
    entity_class = entities.Comment
    endpoint = "/v1/comment"
    list_body = {
        "limit": 20,
    }
    list_suffix = "list-primary"
