from datetime import datetime

from .base import Base
from .user import User


class Comment(Base):
    def __init__(
        self,
        id: str,
        owner: dict[str, str] = {},
        pid: str = "",
        author: dict = {},
        text: str = "",
        level: int = 0,
        likeCount: int = 0,
        createdAt: str = "",
        entities: list[dict] = [],
        replyCount: int = 0,
        threadReplyCount: int = 0,
        replies: list[dict] = [],
        replyToComment: dict = {},
        # HELP WANTED: voice comment structure, welcome to contribute
        **kwargs,
    ):
        super().__init__(id=id)
        self.owner = owner
        self.pid = pid
        self.author = User(**author) if author else None
        self.text = text
        self.level = level
        self.like_count = likeCount
        self.created_at = datetime.fromisoformat(createdAt) if createdAt else None
        self.entities = entities
        self.reply_count = replyCount
        self.thread_reply_count = threadReplyCount
        self.replies = [Comment(**reply) for reply in replies]
        self.reply_to_comment = Comment(**replyToComment) if replyToComment else None
        # set rest keys as attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self) -> str:
        return f"Comment(id={self.id}, text={self.text})"
