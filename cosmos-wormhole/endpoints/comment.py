from typing import AsyncGenerator, Literal

import entities

from .base import Base


class Comment(Base[entities.Comment]):
    entity_class = entities.Comment
    endpoint = "/v1/comment"
    list_body = {
        "limit": 20,
    }
    list_suffix = "list-primary"

    def list_by_episode(
        self, episode_id: str, order: Literal["HOT"] = "HOT"
    ) -> AsyncGenerator[entities.Comment, None]:
        return self.list(
            {"order": order, "owner": {"type": "EPISODE", "id": episode_id}}
        )
