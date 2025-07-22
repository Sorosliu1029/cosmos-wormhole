from typing import AsyncGenerator

from .. import entities
from .base import ListBase


class Followee(ListBase[entities.User]):
    entity_class = entities.User
    endpoint = "/v1/user-relation"
    list_suffix = "list-following"

    def list_following(self, user_id: str) -> AsyncGenerator[entities.User, None]:
        return self.list({"uid": user_id})


class Follower(ListBase[entities.User]):
    entity_class = entities.User
    endpoint = "/v1/user-relation"
    list_suffix = "list-follower"

    def list_follower(self, user_id: str) -> AsyncGenerator[entities.User, None]:
        return self.list({"uid": user_id})
