from typing import AsyncGenerator, Literal

import entities

from .base import ListBase


class Comment(ListBase[entities.Comment]):
    entity_class = entities.Comment
    endpoint = "/v1/comment"
    list_body = {"limit": 20}
    list_suffix = "list-primary"

    def list_by_episode(
        self, episode_id: str, order: Literal["HOT", "TIMESTAMP", "TIME"] = "HOT"
    ) -> AsyncGenerator[entities.Comment, None]:
        return self.list(
            {"order": order, "owner": {"type": "EPISODE", "id": episode_id}}
        )


class Reply(ListBase[entities.Comment]):
    entity_class = entities.Comment
    endpoint = "/v1/comment"
    list_body = {}
    list_suffix = "list-thread"

    def list_by_comment(
        self, comment_id: str, order: Literal["SMART", "TIME"] = "SMART"
    ) -> AsyncGenerator[entities.Comment, None]:
        return self.list({"primaryCommentId": comment_id, "order": order})
